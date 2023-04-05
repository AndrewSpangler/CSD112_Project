import os
import sys
import importlib.util
from flask import Flask

# List to store dynamically loaded blueprints
blueprints = []

app = Flask(__name__)
# This list is populated by dynamic modules
# It it used by templates to create a nav bar
app.menu_items = []
# This variable is updated when the user selects an item in the navigation bar
app.selected = ""

@app.route('/')
def index():
    return 'Hello world!'

# context processor which runs before any template is rendered
# Provides the menu items and current selection
@app.context_processor
def provide_selection():
    return dict(menu_items=app.menu_items, selected=app.selected)

# Import dynamic modules
modules = []
for entry in os.scandir("modules"):
    if entry.isdir(): # Ignore files in modules folder
        module = os.path.join("modules", entry.name, "module.py")
        if os.path.isfile(module):
            spec = importlib.util.spec_from_file_location(
                entry.name,
                module
            )
            module = importlib.util.module_from_spec(spec)
            modules.append(module)

# Sort modules by priority
modules = sorted(modules, key=lambda module: module.priority)

# Load in modules
for module in modules:
    module.load(app)
