import json
from hashlib import md5
import base64

import time
import datetime


def format_md5(obj):
    parser = md5()
    parser.update(obj.encode('utf-8'))
    return parser.hexdigest()


def random_password():
    seed = int(time.time() * 1000)
    return format_md5(str(seed))


def now():
    return int(''.join(str(time.time()).split('.'))[:10])


def base64_decode_dict(obj):
    return json.loads(base64.decodebytes(obj if isinstance(obj, bytes) else obj.encode()).decode())


def base64_encode_dict(obj):
    return base64.encodebytes(json.dumps(obj).encode()).decode()


def convert_timestamp(date, format_type="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(datetime.datetime.strptime(date, format_type).timetuple()))
