from flask import Blueprint, render_template

priority = 0 # Always load this module first

blueprint = Blueprint(
    "Index",
    __name__,
    static_folder="static",
    template_folder="templates"
)

def load(app):
    @blueprint.route("/")
    def index():
        app.selected = "Index"
        return render_template("index.html")

    app.register_blueprint(blueprint)
    app.menu_items.append("Index")
