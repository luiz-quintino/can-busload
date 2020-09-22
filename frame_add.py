import tkinter as tk
import const as Const
import frame_config as ConfigFrame, scrowframe as ScrollFrame
import drawble as r


class AddList(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky='nwes')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # INITIALIZE VARIABLES
        self.child = child
        self.lbl_sel_item_lst = []  # label list_frame of selected items
        self.sel_items = {}  # list os selected items
        self.sel_item_id = 0  # last index of label_frame selected item

        self.auto_id = 0x400 if child.cnf['id_size'] == 'Force 11 bits' else 0x8000000
        self.auto_cycle = 100
        self.auto_size = 8
        self.base_name = 'MY_NEW_MESSAGE_'

        self.txt_search = tk.StringVar()  #
        self.txt_cycle = tk.StringVar()
        self.txt_size = tk.StringVar()
        self.txt_name = tk.StringVar()
        self.txt_id = tk.StringVar()

        self._get_config()

        msg = ['Auto generate helps to fulfill the fields faster',
               'Clik on the message on the list to remove it',
               'Removed message is moved to the fields to make changes, if needed']
        self.child.status_bar_list(msg)

        # IMAGES
        self.img = {
            Const.IMG_PLUS: tk.PhotoImage(file=r.IMG_PLUS),
            Const.IMG_AUTO: tk.PhotoImage(file=r.IMG_SPARK),
        }

        # LABEL
        tk.Label(self, text='Messages added').grid(column=0, row=0, padx=(20, 0), pady=(12, 0), columnspan=2,
                                                   sticky='w')
        tk.Label(self, text='cycle time   msg size').grid(column=1, row=0, columnspan=3, pady=(12, 0), padx=(0, 35),
                                                          sticky='e')
        tk.Label(self, text='Auto generate values').grid(column=0, row=3, padx=(20, 5), sticky='w')
        tk.Label(self, text='ID (hexadecimal)').grid(column=0, row=4, padx=(20, 5), sticky='w')
        tk.Label(self, text='Message name').grid(column=0, row=5, padx=(20, 5), sticky='w')
        tk.Label(self, text='Cycle time (ms)').grid(column=0, row=6, padx=(20, 5), sticky='w')
        tk.Label(self, text='size (bytes)').grid(column=0, row=7, padx=(20, 5), sticky='w')
        tk.Label(self, text='Add message').grid(column=0, row=8, padx=(20, 0), pady=(12, 0), sticky='w')

        # ENTRY
        tk.Entry(self, width=10, textvariable=self.txt_id).grid(column=1, row=4, sticky='we')
        tk.Entry(self, width=35, textvariable=self.txt_name).grid(column=1, row=5, columnspan=2, padx=(0, 20),
                                                                  sticky='we')
        tk.Entry(self, width=4, textvariable=self.txt_cycle).grid(column=1, row=6, padx=(0, 20), sticky='we')
        tk.Entry(self, width=4, textvariable=self.txt_size).grid(column=1, row=7, padx=(0, 20), sticky='we')

        self._update_selected_message()

        # BUTTONS
        tk.Button(self, imag=self.img[Const.IMG_PLUS],
                  command=lambda: self._button_add_message()) \
            .grid(column=1, row=8, padx=(2, 20), sticky='w')

        tk.Button(self, imag=self.img[Const.IMG_AUTO],
                  command=lambda: self._generate_data()) \
            .grid(column=1, row=3, padx=(2, 20), sticky='w')
        tk.Button(self, text="Clear list",
                  command=lambda: self._button_clear_list()) \
            .grid(column=1, row=2, columnspan=2, padx=(2, 20), pady=(2, 0), sticky='e')
        tk.Button(self, text="Cancel",
                  command=lambda: self._button_cancel()) \
            .grid(column=0, row=9, padx=(20, 0), pady=(10, 5), sticky='w')
        tk.Button(self, text="Confirm",
                  command=lambda: self._button_confirm()) \
            .grid(column=1, row=9, columnspan=2, padx=(0, 20), pady=(10, 5), sticky='e')

    def _update_selected_message(self):
        try:
            self.fselected.destroy()
        except Exception as e:
            print(e)

        self.fselected = ScrollFrame.VerticalScrolledFrame(self, height=200, width=200, borderwidth=2, relief=tk.GROOVE)
        self.fselected.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=(20, 20))
        self.sel_item_id = 0
        for name, values in self.sel_items.items():
            self.lbl_sel_item_lst.insert(self.sel_item_id, [])
            self.lbl_sel_item_lst[self.sel_item_id] = tk.Label(self.fselected, text="{:50}".format(name))
            self.lbl_sel_item_lst[self.sel_item_id].bind("<Button-1>", lambda e, index = self.sel_item_id: self._on_click_remove_item_label_frame(e, index))
            self.lbl_sel_item_lst[self.sel_item_id].grid(column=1, row=self.sel_item_id, sticky='w')
            tk.Label(self.fselected, text="{:6}".format(values[0])).grid(column=0, row=self.sel_item_id, sticky='w')
            tk.Label(self.fselected, text="{:5}".format(values[2])).grid(column=2, row=self.sel_item_id, sticky='w')
            tk.Label(self.fselected, text="{:3}".format(values[1])).grid(column=3, row=self.sel_item_id, sticky='w')
            self.sel_item_id += 1

    def _get_config(self):
        self.sel_items = self.child.cnf['add_message'].copy()

    def _add_selected_item(self):
        if self._validate_input():
            self.sel_items.update({self.txt_name.get(): [str(int(self.txt_id.get(), 16)), self.txt_size.get(), self.txt_cycle.get()]})
            self.auto_cycle = self.txt_cycle.get()
            self.auto_size = self.txt_size.get()
            self.auto_id = int(self.txt_id.get(), 16)
            self._update_selected_message()

    def _validate_input(self):
        err = []
        size = self.txt_size.get()
        cycle = self.txt_cycle.get()
        name = self.txt_name.get()
        frame_id = self.txt_id.get()
        if len(size) == 0:
            size = -1
        else:
            size = int(size)
        if len(cycle) == 0:
            cycle = -1
        else:
            cycle = int(cycle)
        if size < 0 or size > 8:
            err.append('Wrong message size')
        if cycle <= 0 or cycle > 10000:
            err.append('Wrong message cycle time')
        if len(name) == 0:
            err.append('Wrong message name')
        if len(frame_id) == 0:
            err.append('Wrong message id')
        if err:
            self.child.status_bar_text(err)
            return False
        return True

    def _remove_selected_item(self, name):
        self.txt_name.set(name)
        self.txt_id.set(self.sel_items[name][0])
        self.txt_size.set(self.sel_items[name][1])
        self.txt_cycle.set(self.sel_items[name][2])
        self.sel_items.pop(name)
        self._update_selected_message()

    def _on_click_remove_item_label_frame(self, position, index):
        """py = self.fselected.inner.winfo_pointery()
        index = (py - self.winfo_rooty() - self.fselected.outer.winfo_y() - 7 - self.fselected.inner.winfo_y()) // 21"""
        m = self.lbl_sel_item_lst[index].cget('text')
        self._remove_selected_item(m.strip())

    def _generate_data(self):
        if not self.txt_cycle.get():
            self.txt_cycle.set(self.auto_cycle)
        if not self.txt_size.get():
            self.txt_size.set(self.auto_size)
        self.txt_name.set(self._get_auto_name())
        self.txt_id.set(hex(self._get_auto_id()))

    def _get_auto_name(self):
        index = 1
        valid = False
        while not valid:
            name = self.base_name + "{:03}".format(index)
            valid = self._valid_name(name)
            index += 1
            if index >= 1000:
                self.base_name = 'MY_NEW_MESSAGE_EXTRA_'
                index = 1
        return name

    def _valid_name(self, name):
        for msg in self.child.dbc.messages:
            if msg.name == name:
                return False
        for msg in self.sel_items.keys():
            if msg == name:
                return False
        return True

    def _get_auto_id(self):
        valid = False
        index = self.auto_id
        while not valid:
            valid = self._valid_id(str(index))
            limit = (0x800 if self.child.cnf['id_size'] == 'Force 11 bits' else 0x9000000)
            if self.auto_id >= limit:
                index = (0x400 if self.child.cnf['id_size'] == 'Force 11 bits' else 0x8000000)
            index += 1
        self.auto_id = index
        return self.auto_id - 1

    def _valid_id(self, frame_id):
        for msg in self.child.dbc.messages:
            if msg.id == frame_id:
                return False
        for msg in self.sel_items.values():
            if msg[0] == frame_id:
                return False
        return True

    def _button_add_message(self):
        self._add_selected_item()
        self._clear_fields()

    def _clear_fields(self):
        self.txt_cycle.set('')
        self.txt_size.set('')
        self.txt_name.set('')
        self.txt_id.set('')

    def _button_clear_list(self):
        self.sel_items.clear()
        self._update_selected_message()

    def _button_confirm(self):
        self.child.cnf['add_message'] = self.sel_items.copy()
        self.child.on_modify_config()
        self._button_cancel()

    def _button_cancel(self):
        self.child.switch_frame(ConfigFrame.StartPage)
