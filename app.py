from flask import Flask
from config import HOST, PORT, DEBUG



class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',
        variable_end_string='%%'
    ))


app = CustomFlask(__name__, static_folder='static')
app.config.from_object('config')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG, processes=10)

