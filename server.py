
from flask import Flask, request
import json
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from bench import Bench
from constants import Constants

# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
# static_folder = "dist"
# app = Flask(__name__,static_folder=static_folder, template_folder=tmpl_dir)
app = Flask(__name__)
app.debug = False

bench = Bench()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/ar/init-files", methods=['POST'])
def ar_init_files():
    print(ar_init_files.__name__)
    bench.init_files()
    return json.dumps({
        "status": Constants.RESULT_OK,
        "message": "ok"
    })


@app.route("/ar/calibration-data-array", methods=['POST'])
def ar_calibration_data_array():
    print(ar_calibration_data_array.__name__)
    json_data = request.json
    bench.write_array(json_data)
    return json.dumps({
        "status": Constants.RESULT_OK,
        "message": "ok"
    })


if __name__ == '__main__':
    port = 8101
    print("server starting on port: ", port)
    server = pywsgi.WSGIServer(('0.0.0.0', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
