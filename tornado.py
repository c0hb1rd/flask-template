from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_socket import fk_socket


http_server = HTTPServer(WSGIContainer(fk_socket.socket))
http_server.listen(12345)
IOLoop.instance().start()
