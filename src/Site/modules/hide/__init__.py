import os
from flask import Blueprint, render_template

priority = 150 

blueprint = Blueprint(
    "Hide",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

def load(app):
    @blueprint.route("/ide")
    def ide():
        app.selected = "IDE"
        return render_template("ide.html")

    app.register_blueprint(blueprint)
