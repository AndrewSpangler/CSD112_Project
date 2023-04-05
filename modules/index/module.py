from flask import Blueprint, render_template

blueprint = Blueprint(
    "index",
    __name__,
    static_folder="static",
    template_folder="templates"
)


@blueprint.route("/")
def index():
    return render_template("index.html")


def load(app):
    app.register_blueprint(blueprint)
