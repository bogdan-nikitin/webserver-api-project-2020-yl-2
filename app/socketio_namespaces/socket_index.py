from flask_socketio import join_room, leave_room, send, Namespace, emit


class IndexNamespace(Namespace):
    pass
    # def on_connect(self):
    #     join_room('test')
    #     pass
    #
    # def on_disconnect(self):
    #     pass
    #
    # def on_my_event(self, data):
    #     print('hi')
    #     emit('my_response', data)
    #
    # def on_my_response(self, data):
    #     print('my_response', data)
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
