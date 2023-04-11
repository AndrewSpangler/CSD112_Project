import os
from flask import Blueprint, render_template, redirect

priority = 300

blueprint = Blueprint(
    "Github",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


def load(app):
    @blueprint.route("/github")
    def github():
        return redirect(app.settings.github_url, code=302)

    # Add item to top nav
    app.menu_items.append(
        (
            "GITHUB",
            "Github.github",
        )
    )
    app.register_blueprint(blueprint)
