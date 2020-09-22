class Node:
    def __init__(self, name):
        self.name = name
        self.tx = []
        self.rx = []


class Message:
    def __init__(self, id):
        self.name = ''
        self.id = id
        self.size = 0
        self.cycle = 0
        self.senders = []
        self.receivers = []
        self.fd = False
        self.format = ''


COMMAND_LIST = ['BS_', 'BU_', 'BO_', 'SG_', 'BO_TX_BU_', 'BA_']
last_id = ''
MSG_FORMAT = {'0': 'CAN', '1': 'EXTENDED CAN', '14': 'CAN FD', '15': 'EXTENDED CAN FD'}


class Parser:
    def __init__(self, file):
        self.nodes = []
        self.messages = []
        self.bus_type = ''
        self.bd_name = ''
        self._parse(self._open_dbc(file))

    def get_node_tx(self, node):
        node = node.upper().strip()
        for item in self.nodes:
            if node == item.name:
                return item.tx
        return []

    def get_node_rx(self, node):
        node = node.upper().strip()
        for item in self.nodes:
            if node == item.name:
                return item.rx
        return []

    def get_message_senders(self, msg):
        msg = msg.upper().strip()
        for item in self.messages:
            if msg == item.name:
                return item.senders
        return []

    def get_message_receivers(self, msg):
        msg = msg.upper().strip()
        for item in self.messages:
            if msg == item.name:
                return item.receivers
        return []

    def get_message_info(self, msg):
        msg = msg.upper().strip()
        for item in self.messages:
            if msg == item.name:
                return [item.id, item.name, item.cycle, item.size]
        return []

    def _open_dbc(self, dbc):
        try:
            with open(dbc) as file_obj:
                dbc_obj = file_obj.readlines()
                return dbc_obj
        except Exception as e:
            print('Erro \n{}'.format(e))
            return []

    def _add_node(self, nodes):
        for item in nodes:
            self.nodes.append(Node(item))

    def _add_node_tx(self, node, msg):
        for id in range(len(self.nodes)):
            if self.nodes[id].name in node and msg not in self.nodes[id].tx:
                self.nodes[id].tx.append(msg)

    def _add_node_rx(self, node, msg):
        for id in range(len(self.nodes)):
            if self.nodes[id].name in node and msg not in self.nodes[id].rx:
                self.nodes[id].rx.append(msg)

    def _add_message(self, msg):
        message = Message(msg[0])
        message.name = msg[1]
        message.size = int(msg[2])
        senders = msg[3].split(',')
        message.senders = message.senders + senders
        self.messages.append(message)

    def _set_msg_format(self, last_id, format):
        for id in range(len(self.messages)):
            if self.messages[id].id == last_id:
                self.messages[id].format = MSG_FORMAT.get(format)
                if format == '14' or format == '15':
                    self.messages[id].fd = True
                break

    def _set_msg_cycle(self, last_id, cycle):
        for id in range(len(self.messages)):
            if self.messages[id].id == last_id:
                self.messages[id].cycle = int(cycle)
                break

    def _add_receiver(self, last_id, node):
        list = node.split(',')
        for id in range(len(self.messages)):
            if self.messages[id].id == last_id:
                for node in list:
                    if node not in self.messages[id].receivers:
                        self.messages[id].receivers.append(node)
                self._add_node_rx(node, self.messages[id].name)
                break

    def _add_senders(self, last_id, node):
        for id in range(len(self.messages)):
            if self.messages[id].id == last_id:
                if node not in self.messages[id].senders:
                    self.messages[id].senders.append(node)
                self._add_node_tx(node, self.messages[id].name)
                break

    def _parse(self, dbc_file):
        if dbc_file:
            for line in dbc_file:
                self._get_command(line)

    def _get_command(self, line):
        line = line.replace(':', ' ').strip()
        if len(line) == 0:
            return

        line = self._my_split(line)

        command = line[0]
        if command in COMMAND_LIST and len(line) > 1:
            self._get_parameters(command, self._clean_up(line[1:]))

    def _my_split(self, line):
        list = []
        word = ''
        delimiters = ['"', ' ', ':', ';']
        aspas = False
        for char in line:
            if char in delimiters:
                if char == '"' and aspas:
                    aspas = False
                    list.append(word)
                    word = ''

                elif char == '"' and not aspas:
                    aspas = True

                elif aspas:
                    word += char

                else:
                    if word:
                        list.append(word)
                        word = ''
            else:
                word += char
        if word:
            list.append(word)

        return  list

    def _clean_up(self, list):
        return list
        empty = list.count('')
        for loop in range(empty):
            list.remove('')
        return list

    def _get_parameters(self, command, line):
        global last_id

        # Nodes
        if command == 'BU_':    # BU_: New_Node_3 New_Node_2 New_Node_1
            self._add_node(line)

        # Messages
        elif command == 'BO_':  # BO_ 1 New_Message_2: 2 Vector__XXX
            self._add_message(line)
            last_id = line[0]
            self._add_node_tx(line[3], line[1])

        # Message's Signal
        elif command == 'SG_':  # SG_ New_Signal_2 : 0|8@1- (1,0) [0|0] "" Vector__XXX
            self._add_receiver(last_id, line[5])

        # Message's Signal
        elif command == 'BO_TX_BU_':  # BO_TX_BU_ 0 : New_Node_2,New_Node_3,New_Node_1;
            nodes = line[1].replace(';','').split(',')
            for item in nodes:
                self._add_senders(line[0], item)

        # Message's CAN type FD = 14 and 15
        elif command == 'BA_':  # BA_ "VFrameFormat" BO_ 0 14; ['"VFrameFormat"', 'BO_', '0', '14;']
            sub_command = line[0]
            if sub_command == 'VFrameFormat':
                if line[1] == 'BO_':
                    self._set_msg_format(line[2], line[3])

            elif sub_command == 'BusType':
                self.bus_type = line[1]

            elif sub_command == 'DBName':
                self.bd_name = line[1]

            elif sub_command == 'GenMsgCycleTime':      #BA_ "GenMsgCycleTime" BO_ 1050 123;
                if line[1] == 'BO_':
                    self._set_msg_cycle(line[2], line[3])


def main():
    dbc_file = ('PWL21_E2A_R1_CANFD3.dbc')
    #dbc_file = ('PWL21_E2A_R1_CANFD8.dbc')
    #dbc_file = ('P521MCA_BH.dbc')
    #dbc_file = ('P521MCA_C.dbc')
    dbc_file = ('DBC/P521MCA_BH-CAN [07338]_4A_R1.DBC')
    dbc = Parser(dbc_file)

    for node in dbc.nodes:
        print([node.name, node.tx, node.rx])

    for message in dbc.messages:
        print([message.id, message.name, message.cycle, message.size, message.format, message.senders, message.receivers])
    print(len(dbc.messages))
    print(len(dbc.nodes))
    #print([dbc.bd_name,dbc.bus_type])

    print([dbc.nodes[0].name,dbc.nodes[1].name])

    print(dbc.get_node_tx('sgw'))
    print(dbc.get_node_rx('sgw'))
    print(dbc.get_message_receivers('body6') + dbc.get_message_senders('BODY6'))
    print(dbc.get_message_info('NWM_VTM'))


if __name__ == '__main__':
    main()




