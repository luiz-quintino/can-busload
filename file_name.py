"""
Busload calc version 2.0
autho: Luiz Quintino
email: luiz.quintino@gmail.com
"""

import os

DBC_PATH = 'dbc/'
OUTPUT_PATH = 'output/'
RES_PATH = 'output/res/'
IMG_PATH = 'img/'
CONFIG_PATH = 'configs/'
INIT_PATH = ''

EXT_CONFIG = '.cnf'
EXT_HTML = '.html'
EXT_CSV = '.csv'
EXT_IMG = '.png'
EXT_DBC = '.dbc'
EXT_INIT = '.init'


class FileName:
    def __init__(self, input_name):
        self.input_name = input_name.lower().strip()
        self._get_name(input_name)

    def _init(self):
        self.file_name = ''
        self.file_path = ''
        self.file_extension = ''

    def get_full_name(self):
        return self.file_path + self.file_name + self.file_extension

    def get_html_full_name(self, file=''):
        if file == '':
            file = self.file_name
        return OUTPUT_PATH + file + EXT_HTML

    def get_csv_full_name(self, file=''):
        if file == '':
            file = self.file_name
        return OUTPUT_PATH + file + EXT_CSV

    def get_dbc_full_name(self, file=''):
        if file == '':
            file = self.file_name
        return DBC_PATH + file + EXT_DBC

    def get_config_full_name(self, file=''):
        if file == '':
            file = self.file_name
        return CONFIG_PATH + file + EXT_CONFIG

    def update(self):
        self._get_name(self.input_name)

    def _get_name(self, title_input):
        self._init()
        title = title_input.strip().lower()
        if title:
            each = title.split('/')
            if len(each) > 0:
                if '.' in each[-1]:
                    ext = each.pop(-1)
                    ext = ext.split('.')
                    if ext[-1]:
                        self.file_extension = '.' + ext.pop(-1)
                    ext = ''.join(ext)
                    if ext:
                        self.file_name = ext
                elif each[-1]:
                    self.file_name = each.pop(-1)
                path = ''.join(each)
                for c in ['|', '<', '>', '*', ':', '"', '?', '\\', ' ']:
                    path.replace(c, '')
                if path:
                    path = '/'.join(each) + '/'
                    for c in ['|', '<', '>', '*', ':', '"', '?', '\\']:
                        path.replace(c, '')
                    main_path = ''
                    bar = chr(92)
                    for i in os.getcwd():
                        if i == bar:
                            main_path += '/'
                        else:
                            main_path += i
                    main_path += '/'
                    path = path[len(main_path):]
                    self.file_path = path

                if not self.file_path and self.file_extension:
                    if self.file_extension == EXT_CONFIG:
                        self.file_path = CONFIG_PATH
                    elif self.file_extension == EXT_DBC:
                        self.file_path = DBC_PATH
                    elif self.file_extension == INIT_PATH:
                        self.file_path = EXT_INIT
                    else:
                        self.file_path = OUTPUT_PATH
