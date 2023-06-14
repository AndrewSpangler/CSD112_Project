import os
import json
from flask import Blueprint, render_template
from datetime import datetime

priority = 100

MAX_PROJECTS_SHOWN = 10

# I am doing some magic here to basicly blend two blueprints together by mounting both at /projects
# This allows me to access both static folders from any template used by a /projects url
blueprint = Blueprint(
    "Projects",
    __name__,
    url_prefix="/projects",
    static_folder=os.path.join(os.getcwd(), "site_data/projects/static"),
    static_url_path="/static/projects",
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)
blueprint2 = Blueprint(
    "Projects2",
    __name__,
    url_prefix="/projects",
    static_folder=os.path.join(os.getcwd(), "site_data/projects/static"),
    template_folder=os.path.join(os.getcwd(), "site_data/projects/templates"),
)



def load(app):
    def get_projects_data():
        projects_data = []
        for entry in os.scandir("site_data/projects"):
            if entry.name.endswith(".json"):
                name = os.path.splitext(entry.name)[0]
                if name.startswith("~"):
                    continue  # Ignores projects that start with ~
                try:
                    with open(entry.path) as f:
                        proj = json.load(f)
                    proj["name"] = name
                    projects_data.append(proj)
                except Exception as e:
                    app.logger.warning(f"Error loading project at {entry.path} - {e}")
                    continue
        for p in projects_data:
            p["details"]=p["details"].replace("\n","<br>")
        # Sort projects by date
        displayed_projects = sorted(projects_data, key=lambda p: p["date"], reverse=True)
        if len(displayed_projects) > MAX_PROJECTS_SHOWN:
            displayed_projects = displayed_projects[:MAX_PROJECTS_SHOWN]
        # Make timestamps friendly
        for p in displayed_projects:
            p["date"] = datetime.utcfromtimestamp(p["date"]).strftime("%b %d '%y")
        # Convert to map for lookup in the project function below
        projects_data = {p["name"]: p for p in projects_data} 
        return projects_data, displayed_projects

    @blueprint.route("/")
    def projects():
        """Projects index page"""
        app.selected = "PROJECTS"
        projects_data, displayed_projects = get_projects_data()
        return render_template("projects.html", projects=displayed_projects)

    @blueprint2.route("/<p_name>")
    def project(p_name):
        """Rendered projects page"""
        app.selected = "None"
        projects_data, displayed_projects = get_projects_data()
        if not p_name in projects_data:
            # Return not found error
            return (
                render_template(
                    "error.html",
                    title="404 - Not Found",
                    error_message=f'Project "{p_name}" could not be found.',
                ),
                404,
            )
        return render_template("project.html", project=projects_data[p_name])

    # Add item to top nav
    app.menu_items.append(("PROJECTS", "Projects.projects"))
    app.register_blueprint(blueprint)
    app.register_blueprint(blueprint2)
