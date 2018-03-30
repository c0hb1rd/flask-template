from core.init_project import create_project
from config import ROOT_PATH

children = [
    {
        'type': 'file',
        'name': '__init__.py'
    },
    {
        'type': 'file',
        'name': 'views.py'
    },
    {
        'type': 'file',
        'name': 'urls.py'
    }
]


def blueprint(name):
    return {
        'type': 'dir',
        'name': name,
        'children': children
    }


project = [{
    'type': 'dir',
    'name': 'blueprint',
    'children': [
        {
            'type': 'file',
            'name': '__init__.py'
        },
        # blueprint("index"),
    ]
}]

create_project(project, ROOT_PATH)
