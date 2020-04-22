from flask_socketio import join_room, leave_room, send, Namespace, emit


class MainNamespace(Namespace):
    @staticmethod
    def on_connect():
        join_room('test')
        print('connect!')
        pass

    @staticmethod
    def on_disconnect():
        pass

    @staticmethod
    def on_my_event(data):
        print('hi')
        emit('my_response', data)

    @staticmethod
    def on_my_response(data):
        print('my_response', data)
#
#
# @socketio.on('my_event', namespace='/')
# def connection(*args, **kwargs):
#     print('Hi!', args, kwargs)
#
#
# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', room=room)
#
#
# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
