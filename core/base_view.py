import json

from flask import request, redirect, session, jsonify
from flask.views import View
from core.dbconnector.conditions import IsCondition

from core.dbconnector import DBResult

from config import GAP, GET, POST
from core.functions import now


def capture_error(func):
    def decorator(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            print(e)
            ret = args[0].error({'info': str(e.args)})

        return ret

    return decorator


def capture_log(func):
    def decorator(*args, **kwargs):
        ret = None

        request_args = request.args.to_dict() if request.method is 'GET' else request.form.to_dict()

        return func(*args, **kwargs) if ret is None else ret

    return decorator


def alter_permission(*args, **options):
    ret = jsonify({'result': 'permission', 'info': 'Not Permission'})
    ret.headers['Access-Control-Allow-Origin'] = 'http://localhost:9999'
    ret.headers['Access-Control-Allow-Methods'] = '*'
    ret.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    ret.headers['Access-Control-Allow-Credentials'] = 'true'

    return ret


def check_session(f):
    def decorator(*args, **kwargs):
        if 'user' not in session:
            return alter_permission()
        return f(*args, **kwargs)

    return decorator


def check_permission(key):
    if key not in session.get('permission', []):
        return alter_permission()
    return 0


class __SimpleView(View):
    json = json
    methods = []
    redirect = redirect
    request = request

    @capture_log
    @capture_error
    @capture_error
    def dispatch_request(self, *args, **kwargs):

        METHOD_META = {
            'GET': self.get,
            'POST': self.post
        }

        if request.method in self.methods:
            return METHOD_META[request.method](*args, **kwargs)
        else:
            return self.error()

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def get_json(self):
        if self.request.data:
            return self.json.loads(self.request.data.decode())

    def get_arg(self, arg=None, default=''):
        if arg is None:
            return self.request.args
        return self.request.args.get(arg, default)

    def get_form(self, arg=None, default=''):
        if arg is None:
            return self.request.form.to_dict()

        return self.request.form.get(arg, default)

    def get_list(self, arg):
        return self.request.form.getlist(arg)

    def require_login(self):
        return self.response('permission')

    def response(self, kind, data=None):
        ret = {'result': kind}

        if isinstance(data, dict):
            ret.update(data)

        ret = jsonify(ret)
        ret.headers['Access-Control-Allow-Origin'] = 'http://localhost:9999'
        ret.headers['Access-Control-Allow-Methods'] = '*'
        ret.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        ret.headers['Access-Control-Allow-Credentials'] = 'true'

        return ret

    def success(self, data=None):
        return self.response("success", data)

    def error(self, data=None):
        return self.response("error", data)

    def warning(self, data=None):
        return self.response("warning", data)

    def process_result(self, ret: DBResult):
        if ret.suc:
            return self.success({
                'data': ret.result,
                'total': ret.rows
            })

        return self.error()


class GetView(__SimpleView):
    methods = GET

    def get(self, *args, **kwargs):
        raise NotImplemented


class PostView(__SimpleView):
    methods = POST

    def post(self, *args, **kwargs):
        raise NotImplemented


class GAPView(GetView, PostView):
    methods = GAP


class SessionGetView(GetView):
    @check_session
    def dispatch_request(self, *args, **kwargs):
        return super(SessionGetView, self).dispatch_request(*args, **kwargs)


class SessionPostView(PostView):
    @check_session
    def dispatch_request(self, *args, **kwargs):
        return super(SessionPostView, self).dispatch_request(*args, **kwargs)


class SessionGAPView(GAPView):
    @check_session
    def dispatch_request(self, *args, **kwargs):
        return super(SessionGAPView, self).dispatch_request(*args, **kwargs)
