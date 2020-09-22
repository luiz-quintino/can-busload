'''
Busload calc version 1.0
autho: Luiz Quintino
email: luiz.quintino@gmail.com
'''
from models.message_out import MessageOut

class MessageList():
    def __init__(self, name, id, messagetime, messageload, dlc, period):
        self.message = MessageOut(name, id, messagetime, messageload, dlc, period)
