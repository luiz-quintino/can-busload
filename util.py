'''
Busload calc version 2.1
autho: Luiz Quintino
email: luiz.quintino@gmail.com

Util library version 1.1
'''

from datetime import datetime
import message_out
from message_out import MessageOut
from statistic import Statistic
import graph
import const as Const
import json
import os
from tkinter import filedialog
from tkinter import BitmapImage
import tkinter as tk

BITMAP = '''#define xlogo16_width 16
        #define xlogo16_height 16
        static char xlogo16_bits[] = {
       0x0f, 0x80, 0x1e, 0x80, 0x3c, 0x40, 0x78, 0x20,
       0x78, 0x10, 0xf0, 0x08, 0xe0, 0x09, 0xc0, 0x05,
       0xc0, 0x02, 0x40, 0x07, 0x20, 0x0f, 0x20, 0x1e,
       0x10, 0x1e, 0x08, 0x3c, 0x04, 0x78, 0x02, 0xf0}
       '''

import dbc_parser


def get_image(image):
    try:
        img = tk.PhotoImage(file=image)
    except:
        img = BitmapImage(data=BITMAP)
        # img = tk.PhotoImage(image=bitmap)
    return img


def get_icon(icon):
    list = [icon, 'busload calc.exe', 'main.exe', 'main.py']
    for file in list:
        if os.path.exists(file):
            return file


def get_welcome_images():
    img_list = []
    if os.path.exists('img/welcome'):
        img_files = os.listdir('img/welcome')
        for img in img_files:
            try:
                image = (tk.PhotoImage(file='img/welcome/' + img))
                img_list.append(image.subsample(2, 2))
            except Exception:
                pass
    return img_list


def event_log(text, config=None):
    logon = True
    if text and logon:
        if config:
            config.log.append(text)


def path_verify(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_db_file(filename, child):
    if os.path.exists(filename):
        try:
            db = dbc_parser.Parser(filename)
            return db
        except Exception as e:
            child.main.main_mesage_box('Error loading dbc file.\n{}'.format(e), Const.MSG_ERROR)
            return []
    else:
        child.main.main_mesage_box('Error loading dbc file.\n File "{}" not found.'.format(filename), Const.MSG_ERROR)
        return []


def get_file(filename):
    try:
        with open(filename) as file_obj:
            lines = file_obj.readlines()
    except:
        return []
    return lines


def save_log(text):
    if not (os.path.exists('log')):
        os.mkdir('log')
    file = filedialog.asksaveasfilename(initialdir="log/",
                                        title="Save log file",
                                        filetypes=[("Text file", "*.txt")])

    if file:
        if not '.txt' in file:
            file += '.txt'
        with open(file, 'w') as file_obj:
            file_obj.write(get_date(2) + "\n")
            file_obj.write(text)


def get_commands(line):
    line = line.lower()
    command = line.split("//")
    command = command[0].split(":")
    if len(command) > 1:
        value = command[1].rstrip().lstrip()
    else:
        value = ''
    command = command[0].rstrip().lstrip()

    if command and value:
        return [command, value]
    elif command in ['[new]', '[calc]']:
        return [command]

    return []


def get_date(format_date=2):
    """
    0 = dd-mm-yyyy
    1 = M d, yyyy
    2 = M d, yyyy H:M:S
    """
    data = datetime.now()

    if format_date == 0:
        data = data.strftime("%Y%m%d_%H%M%S")
    elif format_date == 1:
        data = data.strftime("%B %d, %Y")
    else:
        data = data.strftime("%B %d, %Y %H:%M:%S")

    return data


def create_metadata(name, c):
    meta_data = 'Busload Calc configuration, 2020,' \
                'report_version, 2.1,' \
                'report_name, {},' \
                'label, {},' \
                'dbc, {},' \
                'description, {},' \
                'responsible, {},' \
                'baudrate, {},' \
                'bit_stuffing, {},' \
                'id_size, {},' \
                'yregion, {},' \
                'rregion, {},' \
                'busload_result, {}'.format(name,
                                            c.cnf.get('label') if c.cnf.get('label') else c.cnf.get('dbc'),
                                            c.cnf.get('dbc'),
                                            c.cnf.get('description') if c.cnf.get('description') else "",
                                            c.cnf.get('responsible') if c.cnf.get('responsible') else "",
                                            c.cnf.get('baudrate'),
                                            c.cnf.get('bit_stuffing'),
                                            c.cnf.get('id_size'),
                                            c.yellow,
                                            c.red,
                                            str(c.result[2].busload))
    return meta_data


def save_output_html(name, single_test):
    path_verify('output')
    meta_data = create_metadata(name, single_test)
    try:
        with open(name, 'w') as file_obj:
            # Head configuration and style
            a = '<!doctype html> \n<html lang="en"> \n<head>  <meta charset="utf-8"> \n ' \
                '<title>Busload calculation report 2.1</title> \n<meta name="CAN bus busload calculation" content="The HTML5 Herald">' \
                '<meta author="luiz quintino" content="SitePoint">\n<meta result@busloadcalc="%s"\n><link rel="stylesheet" href="css/styles.css?v=1.0">' % meta_data

            file_obj.write(a)
            a = '<style>\n' \
                '   body {background-color: white;} \n' \
                '   h1 {color: blue;} \n' \
                '   p {color: black;} \n' \
                '   #p01 {color: red;} \n' \
                '   #p02 {color: black; font-size: 8px;text-align: left;} \n' \
                '   #p03 {color: white;padding: 2px;text-align: left;background-color: #4CAF50;border: solid 1px #a6d8a8;width: 70%} \n' \
                '   #p04 {color: white;padding: 2px;text-align: left;background-color: #CD7A7A;border: solid 1px #CD7A7A;width: 70%} \n' \
                '   #p05 {color: black;padding: 2px;text-align: left;background-color: "white";border: solid 1px "black";width: 70%} \n' \
                '   #p06 {color: black;font-size: 12px;text-align: left;} \n' \
                '   #panel3 {display: block;} \n' \
                '   #panel2 {display: block;} \n' \
                '   #panel {display: block;} \n' \
                '   #customers {font-family: "Trebuchet MS", Arial, Helvetica, sans-serif; border-collapse: collapse;width: 60%;} \n' \
                '   #customers td, #customers th {border: 1px solid #ddd; padding: 8px;} \n' \
                '   #customers tr:nth-child(even){background-color: #f2f2f2;} \n' \
                '   #customers tr:hover {background-color: #ddd;} \n' \
                '   #customers th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #A3AFCD; color: white;} \n' \
                '   * {box-sizing: border-box;}\n' \
                '   .row:after {content: "";display: table;clear: both;}\n' \
                '   .column {float: left;width: 30%;padding: 10px; height: auto;}\n' \
                '</style>\n'

            a += '</head>\n' \
                 '<body> \n <script src="js/scripts.js"></script>\n'
            file_obj.write(a)

            # Begin of text
            a = ' <h1> Busload calculation report v.1.2  </h1>\n' \
                '<p>'
            file_obj.write(a)

            if single_test.cnf.get('label'):
                a = '<b>Test title: %s </b>\n<br> ' % single_test.cnf.get('label')
                file_obj.write(a)

            if single_test.cnf.get('description'):
                a = 'Description: %s ' % single_test.cnf.get('description')
                file_obj.write(a)

            # LEFT DIV: result
            value = single_test.result[2]
            a = '</p>\n' \
                '<div class="row"><div class="column"><p> <b> TEST RESULT <br> BUSLOAD: %.2f' % value.busload
            file_obj.write(a)

            dif = value.non_used_messages - value.used_messages
            file_obj.write("% </b></p>\n")

            a = '<dl><dt>\n<b>Configuration </b></dt>\n' \
                '<dd>DBC file: %s </dd>\n' \
                '<dd>Baudrate: %s </dd>\n' \
                '<dd>Bit stuffing addition: %s </dd>\n' \
                '<dd>Identifier: %sbits </dd>\n' \
                '</dl>\n' \
                ' ' % (single_test.cnf['dbc'],
                       single_test.cnf.get('baudrate'),
                       (single_test.cnf.get('bit_stuffing')),
                       single_test.cnf.get('id_size'))
            file_obj.write(a)

            today = get_date()
            a = '<p>Test realized at %s ' % today
            file_obj.write(a)

            if single_test.cnf.get('responsible'):
                a = '<br>Responsible: %s \n' % single_test.cnf.get('responsible')
                file_obj.write(a)

            # RIGHT DIV: Canvas
            a = '</p></div>\n<div class="column"><canvas id="myCanvas" width="250" height="250"></canvas></div></div>\n '
            file_obj.write(a)

            # List of messages
            a = '</p>\n<hr>\n' \
                '<p id="p03" class="flip2" onclick="myFunction2()"> ' \
                'MESSAGES USED TO CALCULATE BUSLOAD %0.0f  \n' % value.used_messages
            a += '<br id="p02">Click to show/hide table</p>\n'
            file_obj.write(a)

            a = '<div id="panel2">\n <TABLE id="customers"> \n' \
                '   <THEAD> \n' \
                '       <TR>\n' \
                '           <TH ROWSPAN=2>Message</TH> \n' \
                '           <TH ROWSPAN=2>time</TH>\n' \
                '           <TH ROWSPAN=2>busload</TH>\n' \
                '       </TR>\n' \
                '   </THEAD> \n'
            file_obj.write(a)

            for item in single_test.result[0]:
                a = '<TR>\n     <TD> %s </TD> <TD> %0.6f </TD> <TD> %0.9f </TD>\n     </TR>\n' % (
                    item.name, item.messagetime, item.messageload)
                file_obj.write(a)
            a = ' </TBODY> \n</TABLE>\n </div>\n'
            a += '<p id="p04" class="flip" onclick="myFunction()"> MESSAGES NOT USED TO CALCULATE BUSLOAD %0.0f \n' % (
                dif)
            a += '<br id="p02" >Click to show/hide table</p>\n'
            file_obj.write(a)

            a = '<div id="panel">\n <TABLE id="customers"> \n' \
                '   <THEAD> \n' \
                '       <TR>\n' \
                '           <TH ROWSPAN=2>Message</TH> \n' \
                '           <TH ROWSPAN=2>cycle time</TH>\n' \
                '       </TR>\n' \
                '   </THEAD> \n'
            file_obj.write(a)

            for item in single_test.result[1]:
                a = '<TR>\n     <TD> %s </TD> <TD> %sms </TD>\n     </TR>\n' % (item.name, item.cycle)
                file_obj.write(a)

            a = '</TBODY> \n </TABLE>\n </div>\n'
            file_obj.write(a)

            # Log file
            a = '<p id="p05" class="flip3" onclick="myFunction3()">click to see the complete log</p>\n' \
                '<p id="p06"> <div id="panel3">'
            file_obj.write(a)

            for log in single_test.log:
                file_obj.write(log + '<br>')

            # JAVASCRIPT
            a = '</div></p>\n' \
                '<script> \nfunction myFunction() { \n' \
                'if (document.getElementById("panel").style.display == "block")\n' \
                'document.getElementById("panel").style.display = "none" \n' \
                'else \n' \
                'document.getElementById("panel").style.display = "block" } \n' \
                'function myFunction2() { \n' \
                'if (document.getElementById("panel2").style.display == "block")\n' \
                'document.getElementById("panel2").style.display = "none" \n' \
                'else \n' \
                'document.getElementById("panel2").style.display = "block" } \n' \
                'function myFunction3() { \n' \
                'if (document.getElementById("panel3").style.display == "block")\n' \
                'document.getElementById("panel3").style.display = "none" \n' \
                'else \n' \
                'document.getElementById("panel3").style.display = "block" } \n'
            file_obj.write(a)

            a = 'var pos = %0.2f;\n' % value.busload
            file_obj.write(a)

            a = 'var busload = "{:0.2f}%";'.format(value.busload)
            file_obj.write(a)

            if single_test.cnf.get('graph') == 'clock':
                a = 'var yb = {}; var rb = {};'.format(single_test.yellow, single_test.red)
                file_obj.write(a)

            a = '\nvar c = document.getElementById("myCanvas"); \nvar ctx = c.getContext("2d");'
            file_obj.write(a)
            a = graph.getType(single_test.cnf.get('graph'))
            file_obj.write(a)
            a = '</script>\n' \
                '</body> \n</html>\n'
            file_obj.write(a)
    except Exception as e:
        return False
    return True


def save_side_report_html(name, files, configs):
    path_verify('output')
    path_verify('output/sbs')
    try:
        with open(name, 'w') as file_obj:
            # Head configuration and style
            output_txt = '<!doctype html> \n<html lang="en"> \n<head>  <meta charset="utf-8"> \n ' \
                         '<title>Busload calculation report</title> \n<meta name="CAN bus busload calculation" content="The HTML5 Herald">' \
                         '<meta name="luiz quintino" content="SitePoint"> \n<link rel="stylesheet" href="css/styles.css?v=1.0"> \n'
            output_txt += '<style>\n' \
                          '   body {background-color: white;} \n' \
                          '   h1 {color: blue;} \n' \
                          '   p {color: black;} \n' \
                          '   #p01 {color: red;} \n' \
                          '   #p02 {color: black; font-size: 8px;text-align: left;} \n' \
                          '   #p03 {color: white;padding: 2px;text-align: left;background-color: #4CAF50;border: solid 1px #a6d8a8;width: 70%} \n' \
                          '   #p04 {color: white;padding: 2px;text-align: left;background-color: #CD7A7A;border: solid 1px #CD7A7A;width: 70%} \n' \
                          '   #p05 {color: black;padding: 2px;text-align: left;background-color: "white";border: solid 1px "black";width: 70%} \n' \
                          '   #p06 {color: black;font-size: 12px;text-align: left;} \n' \
                          '   #customers {font-family: "Trebuchet MS", Arial, Helvetica, sans-serif; border-collapse: collapse;width: 60%;} \n' \
                          '   #customers td, #customers th {border: 1px solid #ddd; padding: 8px;} \n' \
                          '   #customers tr:nth-child(even){background-color: #f2f2f2;} \n' \
                          '   #customers tr:hover {background-color: #ddd;} \n' \
                          '   #customers th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #A3AFCD; color: white;} \n' \
                          '   * {box-sizing: border-box;}\n' \
                          '   .row:after {content: "";display: table;clear: both;}\n' \
                          '   .column {float: left;width: auto;padding: 10px; height: auto;}\n' \
                          '   ul {list-style-type: none;margin: 0;padding: 0;overflow: hidden;background-color: #B1B1CB;}' \
                          '  li {float: left;border-right: 1px solid #bbb;}' \
                          '  li a {display: block;color: white;text-align: center;padding: 14px 16px;text-decoration: none;}' \
                          '  li a:hover {background-color: black;}'
            file_obj.write(output_txt)
            # Configura parametros para javascript
            for i in range(len(files)):
                output_txt = '  #active%s {background-color: #3D37F6; color: white} #panel%s {display: block;}' % (
                    str(i + 1), str(i + 1))
                file_obj.write(output_txt)

            output_txt += '</style>\n</head>\n' \
                          '<body>'  # \n <script src="js/scripts.js"></script>\n'
            file_obj.write(output_txt)

            # Begin of text
            output_txt = ' <h1> Busload calculation report v.2.0  </h1><p>Side by side comparison</p>\n' \
                         '<p> <div class="row"> \n <ul>'
            file_obj.write(output_txt)

            # Cria menu
            i = 0
            for report in files:
                i += 1
                label = configs[report]['label']
                output_txt = '<li><a id="active%s" onclick=myFunction("panel%s","active%s") href="#">%s</a></li>\n' % (
                    str(i), str(i), str(i), label)
                file_obj.write(output_txt)

            output_txt = '</ul>'
            file_obj.write(output_txt)
            i = 0
            for report in files:
                value = float(configs[report]['busload_result'])
                # DIV: Canvas
                i += 1
                output_txt = '<div class="column" id="panel%s"><canvas id="myCanvas%s" width="250" height="250"></canvas>' % (
                    str(i), str(i))
                file_obj.write(output_txt)

                output_txt = '<p>'
                file_obj.write(output_txt)

                output_txt += '<b>Test title: %s </b>\n<br> ' % configs[report]['label']
                output_txt += 'Description: %s ' % configs[report]['description']
                file_obj.write(output_txt)

                output_txt = '<dl><dt>\n<b>Configuration </b></dt>\n' \
                             '<dd>DBC file: {} </dd>\n' \
                             '<dd>Baudrate: {} kbps </dd>\n' \
                             '<dd>Bit stuffing addition: {}%'.format(
                    configs[report]['dbc'].upper(), configs[report]['baudrate'],
                    float(configs[report]['bit_stuffing']))
                output_txt += '</dd>\n'
                file_obj.write(output_txt)

                filename = configs[report]['report_name'].split('/')
                if filename[0] == 'output':
                    file_link = '../../' + configs[report]['report_name']
                else:
                    file_link = configs[report]['report_name']
                output_txt = '<dd>Identifier: %sbits </dd>\n' % configs[report]['id_size']
                output_txt = '<dd>Report: <a href="{0}" target="_blank"> {1} </a></dd>\n'.format(file_link,
                                                                                                 filename[-1])
                file_obj.write(output_txt)

                output_txt = '</dl></p>\n</div>'
                file_obj.write(output_txt)

            output_txt = '</div>'
            file_obj.write(output_txt)
            today = get_date()
            output_txt = '<p>Test realized at %s ' % today
            file_obj.write(output_txt)

            output_txt = '<br>Responsible: %s \n </p>\n' % configs[report]['responsible']
            file_obj.write(output_txt)

            # JAVASCRIPT
            output_txt = '<script> function myFunction(panel,button){ if (document.getElementById(panel).style.display != "none"){document.getElementById(button).style.background = "#7471CA"; document.getElementById(panel).style.display = "none"; }else {document.getElementById(panel).style.display = "block"; document.getElementById(button).style.background = "#3D37F6"; }} '
            file_obj.write(output_txt)

            i = 0
            for report in files:
                i += 1
                output_txt = 'var pos = {0:0.2f}; var busload = "{0:0.2f}%";'.format(
                    float(configs[report]['busload_result']))
                file_obj.write(output_txt)

                output_txt = 'var yb = {}; var rb = {};'.format(configs[report]['yregion'], configs[report]['rregion'])
                file_obj.write(output_txt)

                output_txt = 'var c = document.getElementById("myCanvas%s"); \nvar ' % str(i)
                file_obj.write(output_txt)
                output_txt = graph.getType('clock')
                file_obj.write(output_txt)

            output_txt = '</script>\n' \
                         '</body> \n</html>\n'
            file_obj.write(output_txt)

            return True
    except Exception as e:
        return e


def read_file(file_name):
    try:
        with open(file_name) as file_obj:
            lines = file_obj.readlines()
            return lines
    except Exception as e:
        return ''


def reading_json(file, child):
    try:
        with open(file, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        child.main_mesage_box('Error loading file {}.\n{}'.format(file, e), Const.MSG_ERROR)
        return []


def writing_json(cnf, file, child):
    path_verify('configs')
    try:
        with open(file, 'w') as json_file:
            json.dump(cnf, json_file, indent=4)
    except Exception as e:
        child.main_mesage_box('Error saving config file {}.\n{}'.format(file, e), Const.MSG_ERROR)
        child.saved = False
        return False
    return True


def save_output_csv(name, single_test):
    path_verify('output')
    with open(name, 'w') as file_obj:
        if single_test.cnf.get('label'):
            output_text = "BUSLOAD CALC V.1.1 - : %s " % (
                single_test.cnf.get('label'))
        else:
            output_text = "BUSLOAD CALC V.1.1 "
        file_obj.write(output_text + "\n")

        if single_test.cnf.get('description'):
            output_text = "Description: %-51s " % (
                single_test.cnf.get('description'))
            file_obj.write(output_text + "\n")

        value = single_test.result[2]
        output_text = "BUSLOAD: %0.2f" % value.busload
        dif = value.non_used_messages - value.used_messages
        b = "messages calculated: %.0f messages not used: %0.0f" % (value.used_messages, dif)
        file_obj.write(output_text + "% " + b + "\n")

        output_text = "dbc file: %-56s " % single_test.cnf['dbc']
        file_obj.write(output_text + "\n")

        output_text = "Baudrate: {} kbps bit stuffing addition: {}% identifier: {} bits".format(
            single_test.cnf.get('baudrate'),
            single_test.cnf.get('bit_stuffing'),
            single_test.cnf.get('size_id'))
        file_obj.write(output_text + "\n")

        today = get_date()
        output_text = "Test realized at " + today
        file_obj.write(output_text + "\n")

        if single_test.cnf.get('responsible'):
            output_text = "Test Responsible: %s" % (
                single_test.cnf.get('responsible'))
            file_obj.write(output_text + "\n")

        output_text = "MESSAGE USED TO CALCULATE BUSLOAD"
        file_obj.write(output_text + "\n")

        for item in single_test.result[0]:
            output_text = "Message: %-20s;  time: %0.6f; load: %0.9f;" % (item.name[:19],
                                                                          item.messagetime,
                                                                          item.messageload)
            file_obj.write(output_text + "\n")

        output_text = "MESSAGE NOT USED TO CALCULATE BUSLOAD"
        file_obj.write(output_text + "\n")

        for item in single_test.result[1]:
            output_text = "Message: %-20s; cycle time: %sms" % (item.name[:19],
                                                                item.cycle)
            file_obj.write(output_text + "\n")

    return True


def calc_busload(single_test):
    messages = single_test.dbc.messages
    b11 = 47
    b29 = 65
    bitr = int(single_test.cnf['baudrate'])
    overhead = (b11 if single_test.cnf['id_size'] == 'Force 11 bits' else b29)
    auto_size = False
    if single_test.cnf['id_size'] == 'Auto':
        auto_size = True
    sum_message_load = 0.0
    message_count = 0.0
    bit_stuff = int(single_test.cnf['bit_stuffing']) / 100
    output_list = []
    output_not_used_list = []
    output_ignored = []
    message_time = 0

    for message in messages:
        message_time = 0
        message_load = 0
        if message.name not in single_test.erase_message:
            if message.cycle > 0:
                ml = message.size
                if auto_size:
                    overhead = (b11 if int(message.id) < 2100 else b29)
                message_time = ((ml * 8 + overhead) + ((ml * 8 + overhead - 13) * bit_stuff)) / bitr
                message_load = (message_time / message.cycle)
                sum_message_load += message_load
                message_count += 1
                output_list.append(MessageOut(message.name,
                                              message.id,
                                              message.size,
                                              message.cycle,
                                              message_time,
                                              message_load))
                event_log(output_list[-1])
            else:
                output_not_used_list.append(MessageOut(message.name,
                                                       message.id,
                                                       message.size,
                                                       message.cycle,
                                                       message_time,
                                                       message_load))
                event_log(output_not_used_list[-1])
        else:
            # eventLog("[-] message %s doesn't used in busload calc" % message.name)
            output_not_used_list.append(MessageOut(message.name,
                                                   message.id,
                                                   message.size,
                                                   message.cycle,
                                                   message_time,
                                                   message_load))
            event_log(output_not_used_list[-1])

    result = Statistic(sum_message_load * 100,
                       message_count,
                       len(messages))

    result_output = [output_list,
                     output_not_used_list,
                     result,
                     output_ignored]
    event_log('---> busload: %0.6f' % sum_message_load, single_test)
    single_test.result = result_output


def apply_config(config):
    messages = config.dbc.messages
    # Ecu erase
    config.erase_message = []
    config.log = []

    event_log('Title: {}'.format(config.cnf['label']), config)
    event_log('description: {}'.format(config.cnf['description']), config)
    event_log('responsible: {}'.format(config.cnf['responsible']), config)
    event_log('dbc: {}'.format(config.cnf['dbc']), config)
    event_log('baudrate: {}kbps'.format(config.cnf['baudrate']), config)
    event_log('bit stuffing: {}%'.format(config.cnf['bit_stuffing']), config)
    event_log('id size: {}'.format(config.cnf['id_size']), config)
    event_log('\nAdding message manipulation....\n', config)

    for out in messages:
        for each in config.cnf['erase_ecu']:
            if each[-1] == '*':
                all_mgs = True
                each = each[:-1]
            else:
                all_mgs = False
            if each in out.senders:
                if all_mgs or len(out.senders) == 1:
                    config.erase_message.append(out.name)
                    event_log('[r]:message %s removed from dbc due to %s module removed' % (out.name, each),
                              config)
                else:
                    event_log(
                        "[n]:message %s not removed from dbc due to modules %s are senders" % (out.name, out.senders),
                        config)
                    out.senders.remove(each)

        if out in config.cnf['erase_message']:
            config.erase_message.append(out.name)

    for msg in config.cnf['erase_message']:
        found = False
        for out in messages:
            if out.name == msg:
                event_log('[r]:message %s removed from dbc' % msg, config)
                config.erase_message.append(out.name)
                found = True
                break
        if not found:
            event_log('[n]:message %s not removed from dbc due to message not found' % msg, config)

    # Add messages
    for mes, val in config.cnf['add_message'].items():
        b = message_out.MessageOut(mes, int(val[0]), int(val[1]), int(val[2]))
        messages.append(b)
        event_log('[+]:message %s added with length %s bytes and cycle time %sms' % (mes, val[1], val[2]), config)

    # Modify messages
    for meslist, val in config.cnf['modify_message'].items():
        for out in messages:
            if out.name == meslist:
                event_log('[m]:message %s modifyed from length %s to %s bytes, cycle time %s to %sms' % (
                    out.name, out.size, val[0], out.cycle, val[1]), config)

                config.erase_message.append(out.name)
                b = message_out.MessageOut(out.name + '_edited', out.id, int(val[0]), int(val[1]))
                messages.append(b)
                break

    # Combining dbc
    for mes, val in config.cnf['dbc_combine']['messages'].items():
        b = message_out.MessageOut(val[1], int(val[0]), int(val[3]), int(val[2]))
        if not config.dbc.get_message_info(val[1]):
            messages.append(b)
            event_log('[c]:message %s combined to dbc, with length %s bytes and cycle time %sms' % (val[1], val[3], val[2]), config)
        else:
            event_log('[n]:message %s not combined to dbc due to message already exists in current dbc' % (val[1]), config)

    event_log('\nStarting calculation....', config)
