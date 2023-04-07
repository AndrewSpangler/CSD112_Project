import os
from flask import Blueprint, render_template

priority = 0  # Always load this module first

blueprint = Blueprint(
    "Index",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


def load(app):
    @blueprint.route("/")
    def index():
        app.selected = "Index"
        return render_template("index.html")

    # Add item to top nav
    app.menu_items.append(
        (
            "Index",
            "Index.index",
        )
    )
    app.register_blueprint(blueprint)
