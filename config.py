import os

GET = ['GET']
POST = ['POST']
DELETE = ['DELETE']
PUT = ['PUT']
GAP = GET + POST
METHOD_ALL = GAP + PUT + DELETE


SYS_NAME = ""
ROOT_PATH = os.getcwd()


DB_DATABASE = ''
DB_USER = ''
DB_PASSWORD = ''
DB_CHARSET = ''
DB_DEBUG = False

URL_MAP = []

SECRET_KEY = "A0Zr98j/3yXReGxBT,/gex~XHH!jmN]LWX/,?RT"
DEBUG = True
THREADED = True
HOST = '0.0.0.0'
PORT = 8088
DOMAIN = 'http://{host}:{port}'.format(host=HOST, port=PORT)

CROSS_ADDR = 'http://localhost:9999'

