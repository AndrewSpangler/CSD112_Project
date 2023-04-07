import os
import sys
import json
import importlib.util
import logging
import traceback
from logging.config import dictConfig as logConfig

from flask import Flask

DIR = os.path.dirname(__file__)
TEMPLATES_FOLDER = os.path.join(DIR, "templates")
MODULES_FOLDER = os.path.join(DIR, "modules")

# Configure Logging
logging.basicConfig(level=logging.DEBUG)
logConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(name)s %(threadName)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


class App(Flask):
    def __init__(self, *args, **kwargs):
        Flask.__init__(
            self,
            "Portfolio Site",
            *args,
            template_folder=TEMPLATES_FOLDER,
            **kwargs,
        )
        # Load and set secret key
        # Init secret key in working dir if not already there
        if not os.path.isfile("secret.key"):
            self.logger.info("Creating secret_key")
            with open("secret.key", "w+") as f:
                f.write(str(os.urandom(24).hex()))
        self.logger.info("Loading secret_key")
        with open("secret.key") as f:
            self.config.update({"SECRET_KEY": f.read()})

        # This list is populated by dynamic modules
        # It it used by templates to create a nav bar
        self.menu_items = []
        # This variable is updated when the user clicks a nav item
        self.selected = ""

        # Module loading
        self.logger.info("# Loading dynamic modules.")
        # Load built-in modules
        unloaded = self.get_modules(MODULES_FOLDER, True)
        # Load working dir "hotfix"
        working_dir_modules_folder = os.path.join(os.getcwd(), "modules")
        # In case you are running app from this file's cwd, prevents double-load
        if not working_dir_modules_folder == MODULES_FOLDER:
            unloaded.extend(self.get_modules(working_dir_modules_folder, True))

        modules = []
        module_names = []
        # First pass, sort by module priority
        for m in unloaded:
            try:
                self.logger.info(f"Reading module at {m}")
                # If single-file, module name is file basename
                # If multi-file, module name is dir name
                if m.endswith("__init__.py"):
                    name = os.path.basename(os.path.dirname(m))
                else:
                    name = os.path.basename(m)
                if name in module_names:
                    raise FileExistsError(
                        f"A module with the name {name} has already been loaded"
                    )
                self.logger.info(f"Reading module: {name}")
                spec = importlib.util.spec_from_file_location("load_module", m)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not hasattr(module, "priority"):
                    raise ValueError(f'Module must have a "priority" attribute')
                if not hasattr(module, "load"):
                    raise ValueError(f'Module must have a "load" function')
                modules.append((module, name))
                module_names.append(name)
            except Exception as e:
                self.logger.info(f"Exception loading module at {m} - {e}")
                traceback.print_exc()
                self.logger.info("\n")

        # Sort modules by priority
        modules = sorted(modules, key=lambda m: m[0].priority)
        for m in modules:
            print("Loading", m[1])
            m[0].load(self)

        self.loaded_modules = modules

    def get_modules(self, path: str, verbose: bool = False) -> list:
        """
        Finds modules to load at a given path.
        Either in form {MODULE_NAME}.py or {MODULE_NAME}/__init__.py
        """
        modules = []
        if verbose:
            self.logger.info(f"Searching for modules at - {path}")
        if os.path.isdir(path):
            for e in os.scandir(path):
                if e.is_file() and e.path.endswith(".py"):
                    modules.append(e.path)
                elif e.is_dir() and os.path.isfile(
                    module := os.path.join(e.path, "__init__.py")
                ):
                    modules.append(module)
        elif verbose:
            self.logger.info(f"Failed to locate folder at - {path}")
        if verbose:
            self.logger.info(
                f"Found {len(modules)} modules - {json.dumps(modules, indent=2)}"
            )
        return modules


# Flask object that gets imported by wsgi app
app = App()


# Context processor which runs before any template is rendered
# Provides the menu items and current selection
@app.context_processor
def provide_selection() -> dict:
    return dict(menu_items=app.menu_items, selected=app.selected)


if __name__ == "__main__":
    app.run(use_reloader=False)
