"""
Busload calc version 2.0
autho: Luiz Quintino
email: luiz.quintino@gmail.com
"""


class Statistic:
    def __init__(self, bussload, usedmessage, nonusedmessage, totaltime='', totalmessage=''):
        self.busload = bussload
        self.used_messages = usedmessage
        self.non_used_messages = nonusedmessage
        self.total_time = totaltime
        self.total_message = totalmessage
