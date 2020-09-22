'''
Busload calc version 1.0
autho: Luiz Quintino
email: luiz.quintino@gmail.com
'''
class MessageOut():
    def __init__(self, name, frame_id, length, cycle_time, messagetime=0, messageload=0):
        self.name = name
        self.id = frame_id
        self.messagetime = messagetime
        self.messageload = messageload
        self.size = length
        self.cycle = cycle_time

