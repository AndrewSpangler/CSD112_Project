import os
from flask import Blueprint, render_template, redirect

priority = 200

blueprint = Blueprint(
    "LinkedIn",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


def load(app):
    @blueprint.route("/linkedin")
    def linkedin():
        return redirect(app.settings.linkedin_url, code=302)

    # Add item to top nav
    app.menu_items.append(("LINKEDIN", "LinkedIn.linkedin"))
    app.register_blueprint(blueprint)
