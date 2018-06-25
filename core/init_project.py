import os


def create_dir(directory):
    os.mkdir(directory)


def create_file(path):
    blueprint, dirname, name = path.split(os.sep)[-3:]

    f = open(path, 'w')

    _import = None

    if name == '__init__.py':
        _import = 'from core import BaseBlueprint\nfrom {blueprint}.{dirname} import urls\n\n{dirname}_bp = BaseBlueprint("{dirname}_bp")\n'.format(
            blueprint=blueprint, dirname=dirname)

    if name == 'urls.py':
        _import = 'from core import BaseUrl\nfrom {blueprint}.{dirname} import views\n\n\n'.format(blueprint=blueprint,
                                                                                                   dirname=dirname)

    if name == 'views.py':
        _import = 'from core import *\nfrom model import *\n\n\n'

    if _import:
        f.write(_import)

    f.close()


def create_project(items, parent):
    for item in items:
        path = os.path.join(parent, item['name'])

        if not os.path.exists(path):
            if item['type'] is 'dir':
                create_dir(path)

            if item['type'] is 'file':
                create_file(path)

        if 'children' in item:
            create_project(item['children'], path)
