import os
import sys
import importlib.util
from flask import Flask

# List to store dynamically loaded blueprints
blueprints = []

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'

# Import dynamic modules
modules = []
for entry in os.scandir("modules"):
    if not entry.isdir(): # Ignore files in modules folder
        module = os.path.join("modules", entry.name, "module.py")
        if os.path.isfile(module):
            spec = importlib.util.spec_from_file_location(
                entry.name",
                "/path/to/file.py"
            )
            module = importlib.util.module_from_spec(spec)
            modules.append(module)

# Sort modules by priority
modules = sorted(modules, key=lambda module: module.priority)

# Load in modules
for module in modules:
    module.load(app)
