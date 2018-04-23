import json
from hashlib import md5
import base64

import time
import datetime


def format_md5(s: str):
    parser = md5()
    parser.update(s.encode('utf-8'))
    return parser.hexdigest()


def random_password():
    seed = int(time.time() * 1000)
    return format_md5(str(seed))


def now(length=13, stamp=True, format_type="%Y-%m-%d %H:%M:%S"):
    if stamp:
        return int(''.join(str(time.time()).split('.'))[:length])

    return time.strftime(format_type)


def base64_decode_dict(s):
    return json.loads(base64.decodebytes(s if isinstance(s, bytes) else s.encode()).decode())


def base64_encode_dict(s):
    return base64.encodebytes(json.dumps(s).encode()).decode()


def convert_timestamp(date, format_type="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(datetime.datetime.strptime(date, format_type).timetuple()))
