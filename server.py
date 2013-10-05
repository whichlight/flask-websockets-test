import flask
from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

ws_conns = []

@sockets.route('/echo')
def echo_socket(ws):
    #on connect
    ws_conns.append(ws)

    #while connected
    while True:
        message = ws.receive()
        if message is None:
        #socket has closed/errored
            break
        for c in ws_conns:
            c.send(message)

    #disconnected
    ws_conns.remove(ws)
    ws.close()

@app.route('/')
def hello():
    return flask.render_template('index.html');

#run this with gunicorn gunicorn -k flask_sockets.worker server:app
