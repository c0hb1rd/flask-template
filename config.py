import json
import os

config = {}
config_path = "config.json"

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.loads(f.read(), encoding="utf8")


def config_getter(target, default=None):
    target = target.split("->")

    conf = config
    for item in target:
        conf = conf.get(item, {})

    return conf or default


SYS_NAME = ""
ROOT_PATH = os.getcwd()

DB_DATABASE = config_getter("database->database_name", default="")
DB_USER = config_getter("database->user", default="root")
DB_HOST = config_getter("database->host", default="127.0.0.1")
DB_PORT = config_getter("database->port", default=3306)
DB_PASSWORD = config_getter("database->password", default="")
DB_CHARSET = config_getter("database->charset", default="utf8")
DB_DEBUG = True

URL_MAP = []

SECRET_KEY = "A0Zr98j/3yXReGxBT,/gex~XHH!jmN]LWX/,?RT"
DEBUG = True
THREADED = True
HOST = config_getter("server->host", default="0.0.0.0")
PORT = config_getter("server->port", default=8080)
DOMAIN = 'http://{host}:{port}'.format(host=HOST, port=PORT)
