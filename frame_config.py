import tkinter as tk
from tkinter import ttk
import const as Const
import frame_add, frame_edit, frame_list, frame_dbc_combine
import drawble as r
import util


class StartPage(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky='nwes')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # INITIALIZE VARIABLES
        self.txt = []

        # Create strings to entry's
        for i in range(17):
            self.txt.append(tk.StringVar())

        self.cnf = child.cnf
        self.child = child
        self._get_text_index()  # Get index to json keys
        self._update_values()  # Update entry's values

        # Loop of status bar messages
        msg = ['DBC file is the only required input to perform the busload calc',
               'The configuration changes will not affect the original dbc',
               'Using "Message manipulation" is possible testing variation of the current dbc']
        self.child.status_bar_list(msg)

        # GET ENTRY'S CHANGES
        for entry in self.txt:
            entry.trace('w', lambda name, index, mode, sv=entry: self.on_modify_entry(sv))

        # IMAGES
        self.img = {
            Const.IMG_SETTIGNS: util.get_image(r.IMG_SET),
            Const.SB_ERASE_ECU: util.get_image(r.IMG_DEL_ECU),
            Const.SB_ERASE_MGS: util.get_image(r.IMG_DEL_MSG),
            Const.IMG_AUTO: util.get_image(r.IMG_SPARK),
            Const.IMG_FILE_OPEN: util.get_image(r.IMG_FOLDER),
            Const.IMG_PLUS: util.get_image(r.IMG_PLUS),
            Const.IMG_EDITED: util.get_image(r.IMG_PEN),
            Const.IMG_DBC_COMBINE: util.get_image(r.IMG_DBC_COMBINE),
        }

        # LABEL
        # tk.Label(self, text="Main information").grid(   column=0, row=0, columnspan = 3, sticky='W')
        tk.Label(self, text="Config name").grid(column=0, row=1, sticky='W')
        tk.Label(self, text="DBC file").grid(column=0, row=2, sticky='W')
        tk.Label(self, text="Responsible").grid(column=0, row=3, sticky='W')
        tk.Label(self, text="Title").grid(column=0, row=4, sticky='W')
        tk.Label(self, text="Description").grid(column=0, row=5, sticky='W')
        tk.Label(self, text="Baudrate").grid(column=0, row=6, sticky='W')
        tk.Label(self, text="Bit stuffing").grid(column=0, row=7, sticky='W')
        tk.Label(self, text="Id size").grid(column=0, row=8, sticky='W')
        tk.Label(self, text="Output").grid(column=0, row=9, sticky='W')
        tk.Label(self, text="Graph type").grid(column=0, row=12, sticky='W')
        tk.Label(self, text="Message manipulation").grid(column=0, row=14, columnspan=3, sticky='W')
        tk.Label(self, text="Erase ECU").grid(column=0, row=15, sticky='W')
        tk.Label(self, text="Erase Message").grid(column=0, row=16, sticky='W')
        tk.Label(self, text="Modify Message").grid(column=0, row=17, sticky='W')
        tk.Label(self, text="Add Message").grid(column=0, row=18, sticky='W')
        tk.Label(self, text="Combine dbc").grid(column=0, row=19, sticky='W')

        # ENTRY
        self.configName = tk.Entry(self, textvariable=self.txt[Const.TXT_CONFIG_NAME])
        self.configName.grid(column=1, row=1, columnspan=2, sticky='we')

        tk.Entry(self,
                 textvariable=self.txt[Const.TXT_DBC_FILE]).grid(column=1, row=2, columnspan=2, sticky='we')
        tk.Entry(self,
                 textvariable=self.txt[Const.TXT_RESPONSIBLE]).grid(column=1, row=3, columnspan=2, sticky='we')
        tk.Entry(self,
                 textvariable=self.txt[Const.TXT_TITLE]).grid(column=1, row=4, columnspan=2, sticky='we')
        tk.Entry(self,
                 textvariable=self.txt[Const.TXT_DESCRIPTION]).grid(column=1, row=5, columnspan=3, sticky='we')
        tk.Entry(self, width=10,
                 textvariable=self.txt[Const.TXT_BAUDRATE]).grid(column=1, row=6, sticky='we')
        tk.Entry(self, width=10,
                 textvariable=self.txt[Const.TXT_BIT_STUFFING]).grid(column=1, row=7, sticky='we')
        tk.Entry(self, width=10, state=tk.DISABLED,
                 textvariable=self.txt[Const.TXT_ECU_ERASE]).grid(column=1, row=15, columnspan=2, sticky='we')
        tk.Entry(self, width=10, state=tk.DISABLED,
                 textvariable=self.txt[Const.TXT_MSG_ERASE]).grid(column=1, row=16, columnspan=2, sticky='we')
        tk.Entry(self, width=10, state=tk.DISABLED,
                 textvariable=self.txt[Const.TXT_MSG_MODIFY]).grid(column=1, row=17, columnspan=2, sticky='we')
        tk.Entry(self, width=10, state=tk.DISABLED,
                 textvariable=self.txt[Const.TXT_MSG_ADD]).grid(column=1, row=18, columnspan=2, sticky='we')
        tk.Entry(self, width=10, state=tk.DISABLED,
                 textvariable=self.txt[Const.TXT_DBC_COMBINE]).grid(column=1, row=19, columnspan=2, sticky='we')

        # SCALE - baudrate & bitstuffing
        tk.Scale(self, variable=self.txt[Const.TXT_BAUDRATE],
                 orient=tk.HORIZONTAL, from_=0, to=1000).grid(column=2, row=6, sticky='we')
        tk.Scale(self, variable=self.txt[Const.TXT_BIT_STUFFING],
                 orient=tk.HORIZONTAL, from_=0, to=30).grid(column=2, row=7, sticky='we')

        # CHECKBOX - output
        tk.Checkbutton(self, text='.csv', variable=self.txt[Const.TXT_OUT_CSV],
                       onvalue='true', offvalue='false').grid(column=2, row=9, sticky='w')
        tk.Checkbutton(self, text='html report', variable=self.txt[Const.TXT_OUT_HTML],
                       onvalue='true', offvalue='false').grid(column=1, row=9, sticky='w')

        # RADIOBUTTON - graph and id size
        tk.Radiobutton(self, text='bar', variable=self.txt[Const.TXT_GRAPH],
                       value='bar').grid(column=2, row=12, sticky='w')
        tk.Radiobutton(self, text='clock', variable=self.txt[Const.TXT_GRAPH],
                       value='clock').grid(column=1, row=12, sticky='W')

        '''tk.Radiobutton(self, text='auto', variable=self.txt[Const.TXT_11_BIT],
                       value='11').grid(column=1, row=8, sticky='w')
        tk.Radiobutton(self, text='force 11 bits', variable=self.txt[Const.TXT_11_BIT],
                       value='11').grid(column=1, row=8, sticky='w')
        tk.Radiobutton(self, text='force 29 bits', variable=self.txt[Const.TXT_29_BIT],
                       value='29').grid(column=2, row=8, sticky='w')'''

        # COMBOBOX
        combo = ttk.Combobox(self, textvariable=self.txt[Const.TXT_11_BIT])
        combo['values'] = ('Auto', 'Force 11 bits', 'Force 29 bits')
        combo.state(['readonly'])
        combo.grid(column=1, row=8, columnspan=2, sticky='we')

        for widget in self.winfo_children():
            widget.grid_configure(padx=(20, 0), pady=1)

        # BUTTONS
        tk.Button(self, image=self.img[Const.IMG_AUTO],
                  command=lambda: self._button_auto_config_name()).grid(column=3, row=1, sticky='w')
        tk.Button(self, image=self.img[Const.IMG_FILE_OPEN],
                  command=lambda: self._button_open_dbc()).grid(column=3, row=2, sticky='N,S,W')
        tk.Button(self, image=self.img[Const.SB_ERASE_ECU],
                  command=lambda: self._button_erase_ecu(child)).grid(column=3, row=15, sticky='N,S,W')
        tk.Button(self, image=self.img[Const.SB_ERASE_MGS],
                  command=lambda: self._button_erase_msg(child)).grid(column=3, row=16, sticky='N,S,W')
        tk.Button(self, image=self.img[Const.IMG_EDITED],
                  command=lambda: self._button_modify_msg(child)).grid(column=3, row=17, sticky='N,S,W')
        tk.Button(self, image=self.img[Const.IMG_PLUS],
                  command=lambda: self._button_add_msg(child)).grid(column=3, row=18, sticky='N,S,W')
        tk.Button(self, image=self.img[Const.IMG_DBC_COMBINE],
                  command=lambda: self._button_dbc_combine(child)).grid(column=3, row=19, sticky='N,S,W')
        tk.Button(self, text='Run calc',
                  command=lambda: self._button_run_calc(child)).grid(column=2, row=20, columnspan=2, pady=5, sticky='e')

    def _button_run_calc(self, child):
        child.run_calc()

    def _button_dbc_combine(self, child):
        self.update_config()  # Save current config status
        child.switch_frame(frame_dbc_combine.Combine)

    def _button_auto_config_name(self):
         self.txt[Const.TXT_CONFIG_NAME].set(self.child.get_title())

    def on_modify_entry(self, *args):
        self.child.on_modify_config()

    def _button_open_dbc(self):
        dbc = self.child.open_dbc()
        self.txt[Const.TXT_DBC_FILE].set(dbc.get_full_name().upper())

    def _button_erase_ecu(self, child):
        self.update_config()  # Save current config status
        if self._check_dbc(child):
            child.frm_conf = Const.SB_ERASE_ECU
            child.switch_frame(frame_list.EraseList)

    def _button_erase_msg(self, child):
        self.update_config()  # Save current config status
        if self._check_dbc(child):
            child.frm_conf = Const.SB_ERASE_MGS
            child.switch_frame(frame_list.EraseList)

    def _button_modify_msg(self, child):
        self.update_config()  # Save current config status
        if self._check_dbc(child):
            child.switch_frame(frame_edit.ModifyList)

    def _button_add_msg(self, child):
        self.update_config()  # Save current config status
        if self._check_dbc(child):
            child.switch_frame(frame_add.AddList)

    def _check_dbc(self, child):
        if child.check_dbc():
            if child.dbc:
                return True
            else:
                self.child.status_bar_text("DBC not found or not valid", 5000)
                return False
        self.child.status_bar_text("DBC not found or not valid", 5000)
        return False

    def _update_values(self):
        for k, v in self.cnf.items():
            if k in self.index.keys():
                self.txt[self.index[k]].set(v)
        title = self.child.title()
        if '*' in title:
            title = title[:-1]
        if '.cnf' in title:
            title = title[:-4]
        self.txt[Const.TXT_CONFIG_NAME].set(title)
        # version 2.1
        if not self.cnf.get('dbc_combine'):
            self.cnf['dbc_combine'] = {'dbc_list': [], 'ecus': [], 'messages': {}}
            self.txt[Const.TXT_DBC_COMBINE].set(self.cnf['dbc_combine'])
            self.cnf['version'] = '2.1'
        if str(self.cnf['id_size']) == '11' or self.cnf['id_size'] == '29':
            self.cnf['id_size'] = 'Force {} bits'.format(self.cnf['id_size'])
            self.txt[Const.TXT_11_BIT].set(self.cnf['id_size'])

    def update_config(self):
        for k, v in self.cnf.items():
            if k not in ['add_message',
                         'modify_message',
                         'erase_message',
                         'erase_ecu',
                         'dbc_combine'] and k in self.index.keys():
                self.cnf[k] = self.txt[self.index[k]].get()

    def _get_text_index(self):
        self.index = {
            'dbc': Const.TXT_DBC_FILE,
            'responsible': Const.TXT_RESPONSIBLE,
            'description': Const.TXT_DESCRIPTION,
            'label': Const.TXT_TITLE,
            'bit_stuffing': Const.TXT_BIT_STUFFING,
            'baudrate': Const.TXT_BAUDRATE,
            'id_size': Const.TXT_11_BIT,
            'screen': Const.TXT_OUT_SCREEN,
            'csv': Const.TXT_OUT_CSV,
            'html': Const.TXT_OUT_HTML,
            'modify_message': Const.TXT_MSG_MODIFY,
            'add_message': Const.TXT_MSG_ADD,
            'dbc_combine': Const.TXT_DBC_COMBINE,
            'erase_ecu': Const.TXT_ECU_ERASE,
            'erase_message': Const.TXT_MSG_ERASE,
            'graph': Const.TXT_GRAPH,
        }
