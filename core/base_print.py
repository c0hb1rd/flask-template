from flask import Blueprint
from config import ROOT_PATH


class BaseBlueprint:
    def __init__(self, name):
        self.app = Blueprint(name, __name__, static_folder="assets", template_folder="templates", root_path=ROOT_PATH)

    # Insert url rule into flask url map
    def add_rule(self, url_obj):
        self.app.add_url_rule(url_obj.path, view_func=url_obj.view_obj.as_view(url_obj.view_name))

    # Load url rule map
    def load_rule_maps(self, url_obj_map):
        for url_obj in url_obj_map:
            self.add_rule(url_obj)
