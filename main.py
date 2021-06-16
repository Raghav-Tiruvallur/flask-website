import socketio
from Website import createApp
from flask_socketio import SocketIO,send

app=createApp()

socketio=SocketIO(app)

@socketio.on('message')

def handleMessage(msg):
    print("Message:"+ msg)
    send(msg,broadcast=True)


if __name__=="__main__":
   socketio.run(app,debug=True)

