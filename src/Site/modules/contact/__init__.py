import os
from flask import Blueprint, render_template, request

priority = 1000 

blueprint = Blueprint(
    "Contact",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

def load(app):
    @blueprint.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            return render_template("contact_confirmation.html")
        app.selected = "CONTACT"
        return render_template("contact.html")

    # Add item to top nav
    app.menu_items.append(("CONTACT", "Contact.contact"))
    app.register_blueprint(blueprint)
