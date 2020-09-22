import tkinter as tk
from tkinter import ttk
import const as Const
import frame_config as Config_frame, scrowframe as Scroll_frame
import drawble as r
import util


class Combine(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky='news')

        # INITIALIZE VARIABLES
        self.child = child
        self.lbl_fig_lst = []  # label list_frame of items
        self.lbl_items_list = []  # label list_frame of items
        self.lbl_sel_item_lst = []  # label list_frame of selected items
        item = [k for k in child.cnf['dbc_combine']['messages'].keys()]
        self.sel_items = item    # list os selected items
        self.sel_item_id = 0  # last index of label_frame selected item
        self.searchIndex = 0  # index for consecutive seach
        self.totalItems = 0  # total items in the list
        self.dbc_list = child.cnf['dbc_combine']['dbc_list'].copy()
        self.ecus = child.cnf['dbc_combine']['ecus'].copy()
        self.dbc = None
        self.current_dbc_index = 0
        self.messages = child.cnf['dbc_combine']['messages']

        msg = ['Chose one or more DBCs to combine messages',
               'Select a module on the list to add TX or TX and RX messages',
               'Remove selected messages that are not needed']

        self.child.status_bar_list(msg)

        # IMAGES
        self.img = {
            Const.IMG_EMPTY: util.get_image(r.IMG_GREY),
            Const.IMG_SEND: util.get_image(r.IMG_SEND),
            Const.IMG_SEND_RECEIVE: util.get_image(r.IMG_SEND_RECEIVE),
            Const.IMG_SEND_RECEIVE_GREY: util.get_image(r.IMG_SEND_RECEIVE_GREY),
            Const.IMG_NOT: util.get_image(r.IMG_X),
            Const.IMG_PLUS: util.get_image(r.IMG_PLUS),
            Const.IMG_SEARCH: util.get_image(r.IMG_FOLDER)
        }

        # LABEL
        tk.Label(self, text='DBC list').grid(column=0, row=2, padx=20, pady=(12, 0),
                                             columnspan=2, sticky='w')
        tk.Label(self, text='ECUs').grid(column=0, row=4, padx=20, pady=(12, 0),
                                         columnspan=2, sticky='w')
        tk.Label(self, text='Selected messages').grid(column=0, row=6, padx=20, pady=(12, 0),
                                                      columnspan=2, sticky='w')

        # ENTRY
        self.txtSearch = tk.StringVar()
        self.txtSearch.set('Chose the dbc file...')
        search = tk.Entry(self, textvariable=self.txtSearch)
        search.bind('<1>', lambda e: self._on_click_search())
        search.grid(column=0, row=1, columnspan=2, padx=(20,0), pady=(20,0), sticky='we')

        # LISBOX
        self.list_values = tk.StringVar()
        self.list_box = tk.Listbox(self, listvariable=self.list_values, width=47, height=3, selectmode=tk.SINGLE, borderwidth=1, relief=tk.SUNKEN)
        self.list_box.bind('<<ListboxSelect>>', self._on_select_dbc)
        self.list_box.grid(column=0, row=3, columnspan=2, padx=(20,0), stick='news')
        self.list_values.set(self.dbc_list)

        # SCROLBAR
        s = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.list_box.yview)
        s.grid(row=3, column=2, padx=(0,0), stick='wns')
        self.list_box.configure(yscrollcommand=s.set)

        # VERTICAL SCROWFRAME
        self._update_selected_message()
        self._update_list_frame_ecu(child)

        # BUTTONS
        tk.Button(self, imag=self.img[Const.IMG_SEARCH],
                  command=lambda: self._button_search_dbc()) \
            .grid(column=2, row=1, padx=(2, 0), pady=(20,0),sticky='e')
        tk.Button(self, imag=self.img[Const.IMG_PLUS],
                  command=lambda: self._button_add_dbc_to_list()) \
            .grid(column=3, row=1, padx=(2, 20), pady=(20,0),sticky='e')
        tk.Button(self, imag=self.img[Const.IMG_NOT],
                  command=lambda: self._button_remove_dbc_list()) \
            .grid(column=3, row=3, padx=(2, 20), sticky='ne')
        tk.Button(self, text="Clear all",
                  command=lambda: self._button_clear_all()) \
            .grid(column=1, row=8, columnspan=3, padx=(0, 20), pady=(2, 0), sticky='e')
        tk.Button(self, text="Cancel",
                  command=lambda: self._button_cancel()) \
            .grid(column=0, row=9, padx=(20,0), pady=(10, 5), sticky='w')
        tk.Button(self, text="Confirm",
                  command=lambda: self._button_confirm()) \
            .grid(column=1, row=9, columnspan=3, padx=(0,20), pady=(10, 5), sticky='e')

    def _set_dbc_list(self):
        list=''
        self.list_values.set(list)

    def _button_remove_dbc_list(self):
        try:
            dbc_file = self.list_box.selection_get()
        except Exception as e:
            self.child.main.main_mesage_box('No dbc file selected', Const.MSG_ERROR)
            return

        if dbc_file:
            if self.child.main.main_mesage_box('This process will remove all entries form "{}".\nDo you confirm?'.format(dbc_file), Const.MSG_OK_CANCEL):
                self._remove_dbc(dbc_file)
        else:
            self.child.main.main_mesage_box('Select a dbc file on list to erase')

    def _update_list_frame_ecu(self, child):
        try:
            self.frame.destroy()
        except Exception as e:
            pass

        self.frame = Scroll_frame.VerticalScrolledFrame(self, height=100, width=200, borderwidth=2, relief=tk.SUNKEN)
        self.frame.grid(column=0, row=5, columnspan=3, padx=(20, 20), sticky='nsew')

        if not self.dbc:
            return

        for i in range(len(self.dbc.nodes)):
            self.lbl_fig_lst.insert(i, [])
            self.lbl_items_list.insert(i, [])
            self.lbl_items_list[i] = tk.Label(self.frame, text=str(i) + ": " + self.dbc.nodes[i].name)
            self.lbl_items_list[i].bind("<Button-1>", lambda e, b=i: self._on_click_item_label_frame(e, b))
            self.lbl_items_list[i].bind("<Button-3>", lambda a, b=i: self._on_left_click_item_label_frame(a, b))
            self.lbl_items_list[i].grid(column=1, row=i, sticky='W')

            ecu = '{} {}'.format(self.current_dbc_index, self.dbc.nodes[i].name)
            if (ecu + '*') in self.ecus:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_SEND_RECEIVE])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_SEND_RECEIVE]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')
            elif (ecu + '!') in self.ecus:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_SEND_RECEIVE_GREY])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_SEND_RECEIVE]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')
            elif ecu in self.ecus:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_SEND])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_SEND]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')
            else:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_EMPTY])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_EMPTY]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

        self.totalItems = i

    def _update_selected_message(self):
        try:
            self.frame_selected_items.destroy()
        except Exception as e:
            pass

        self.frame_selected_items = Scroll_frame.VerticalScrolledFrame(self, height=100, width=200,
                                                                       borderwidth=2, relief=tk.GROOVE)
        self.frame_selected_items.grid(column=0, row=7, columnspan=3, sticky='nsew', padx=(20, 20))
        self.sel_item_id = 0
        for name in self.sel_items:
            self.lbl_sel_item_lst.insert(self.sel_item_id, [])
            self.lbl_sel_item_lst[self.sel_item_id] = tk.Label(self.frame_selected_items, text=name)
            self.lbl_sel_item_lst[self.sel_item_id].bind("<Button-1>",
                                                         lambda e: self._on_click_remove_item_label_frame())
            self.lbl_sel_item_lst[self.sel_item_id].grid(column=1, row=self.sel_item_id, sticky='w')
            self.sel_item_id += 1


    def _add_selected_ecu(self, name):
        self.ecus.append(name)

    def _remove_selected_ecu(self, name):
        if name in self.ecus:
            self.ecus.remove(name)

    def _add_selected_item(self, msg_list, ecu):
        for msg in msg_list:
            key = '{:3}: {:5}: {}'.format(self.current_dbc_index, ecu, msg)
            self.sel_items.append(key)
            self.messages[key] = self.dbc.get_message_info(msg)
        self._update_selected_message()

    def _remove_selected_item(self, dbc_index, msg_list, ecu):
        for msg in msg_list:
            item = '{:3}: {:5}: {}'.format(dbc_index, ecu, msg)
            if item in self.sel_items:
                self.sel_items.remove(item)
                a = self.messages.pop(item)
        self._update_selected_message()

    def _empty_icon_in_list(self, item_name, type):
        # type 0 = empty
        # type 1 = <-> grey
        if type == 0:
            self.lbl_fig_lst[self._looking_for_item(item_name)].config(image=self.img[Const.IMG_EMPTY])
        else:
            self.lbl_fig_lst[self._looking_for_item(item_name)].config(image=self.img[Const.IMG_SEND_RECEIVE_GREY])

    def _looking_for_item(self, name, search_type=True):
        # search_type True = search by name, False = search in a list of names
        for index in range(len(self.dbc.nodes)):
            if search_type:
                if self.dbc.nodes[index].name == name:
                    return index
            else:
                if name in self.dbc.nodes[index].name:
                    if self.searchIndex < index:
                        self.searchIndex = index
                        return index

        self.searchIndex = 0  # item not found
        return 0

    def _remove_dbc(self, dbc_file):
        if dbc_file in self.dbc_list:
            self.dbc_list.remove(dbc_file)
            dbc = dbc_file.split(':')
            index = int(dbc[0])
            ecu_list = []
            for ecu in self.ecus:
                ecu_index = ecu.split()
                if index == int(ecu_index[0]):
                    ecu_list.append(ecu)
            for ecu in ecu_list:
                self._remove_selected_ecu(ecu)

            msg_list = []
            for msg in self.sel_items:
                msg_index = msg.split(':')
                if index == int(msg_index[0]):
                    msg_list.append([[msg_index[2].strip()],msg_index[1].strip()])
            for msg in msg_list:
                self._remove_selected_item(index, msg[0], msg[1])
            self.dbc = []
            self._update_list_frame_ecu(self.child)
            self._update_selected_message()
            self.list_values.set(self.dbc_list)
            self.list_box.selection_clear(0, tk.END)

    def _on_select_dbc(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        dbc = value.split(':')
        dbc_file = dbc[1].strip()
        dbc_index = int(dbc[0])
        dbc = util.get_db_file(dbc_file, self.child)
        if dbc:
            self.dbc = dbc
            self.current_dbc_index = dbc_index
            self._update_list_frame_ecu(self.child)
        else:
            if self.child.main_mesage_box('Do you want to remove all entries from this dbc file?', Const.MSG_YES_NO):
                self._remove_dbc(value)
            else:
                self.list_box.selection_clear(0, tk.END)
                self.current_dbc_index = 0

    def _on_click_remove_item_label_frame(self):
        p_inner_pointer_y = self.frame_selected_items.inner.winfo_pointery()
        p_inner_outer_y = self.frame_selected_items.outer.winfo_y()
        p_inner_y = self.frame_selected_items.inner.winfo_y()
        index = (p_inner_pointer_y - self.winfo_rooty() - p_inner_outer_y - 7 - p_inner_y) // 21
        msg = self.lbl_sel_item_lst[index].cget('text')
        m = msg.split(':')
        ecu = '{} {}'.format(m[0].strip(), m[1].strip())

        self._remove_selected_item(int(m[0]), [m[2].strip()], m[1].strip())
        last_message = self._last_message_for_ecu(int(m[0]), m[1].strip())
        print(last_message)
        if ecu in self.ecus:
            self._remove_selected_ecu(ecu)
        elif ecu + '*' in self.ecus:
            self._remove_selected_ecu(ecu + '*')
        elif ecu + '!' in self.ecus:
            self._remove_selected_ecu(ecu + '!')
        if not last_message:
            self._add_selected_ecu(ecu + '!')

        if self.current_dbc_index == int(m[0]) and not last_message:
            self._empty_icon_in_list(m[1].strip(), 1)
        elif last_message:
            self._empty_icon_in_list(m[1].strip(), 0)

    def _last_message_for_ecu(self, dbc_index, ecu):
        item = '{:3}: {:5}:'.format(dbc_index, ecu)
        for msg in self.sel_items:
            if item in msg:
                return False
        return True

    def _on_click_item_label_frame(self, position, index):
        """py = self.frame.inner.winfo_pointery()
        index = (py - self.winfo_rooty() - self.frame.outer.winfo_y() - 7 - self.frame.inner.winfo_y()) // 21"""
        m = self.lbl_items_list[index].cget('text').split()
        m = m[1].strip()  # Get Message name without index number and spaces
        ecu = '{} {}'.format(self.current_dbc_index, m)
        if ecu in self.ecus:  # Put * in ECU from the 'selected list'
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_EMPTY])
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_SEND_RECEIVE])
            self._remove_selected_ecu(ecu)
            self._add_selected_ecu(ecu + '*')
            self._add_selected_item(self.dbc.get_node_rx(m), m)
        elif ecu + '*' in self.ecus:  # Remove ECU from the 'selected list'
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_EMPTY])
            self._remove_selected_ecu(ecu + '*')
            self._remove_selected_item(self.current_dbc_index, self.dbc.get_node_rx(m) + self.dbc.get_node_tx(m), m)
        else:  # ECU not found, ADD it to 'selected list'
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_SEND])
            self._add_selected_ecu(ecu)
            self._remove_selected_item(self.current_dbc_index, self.dbc.get_node_rx(m) + self.dbc.get_node_tx(m), m)
            self._add_selected_item(self.dbc.get_node_tx(m), m)

    def _on_click_search(self):
        if self.txtSearch.get() == 'Chose the dbc file...':
            self.txtSearch.set('')

    def _on_left_click_item_label_frame(self, position, index):
        x = self.frame.inner.winfo_pointerx()
        y = self.frame.inner.winfo_pointery()
        self._popup_window(x, y, index)

    def _popup_window(self, x, y, index):
        # THE CLUE
        self.child.wm_attributes("-disabled", True)
        self.child.main.wm_attributes("-disabled", True)

        title = 'Msg list: {}'.format(self.dbc.nodes[index].name)

        # Creating the toplevel dialog
        self.popup_dialog = tk.Toplevel(self.child)
        self.popup_dialog.title(title)
        self.popup_dialog.geometry('400x200+{}+{}'.format(x, y))
        self.popup_dialog.minsize(200, 200)
        self.popup_dialog.transient(self.child)
        self.popup_dialog.protocol("WM_DELETE_WINDOW", self._close_popup)
        self.popup_dialog.iconbitmap(r.ICO_CHILD)
        self.popup_dialog.columnconfigure(0, weight=1)
        self.popup_dialog.columnconfigure(1, weight=1)
        self.popup_dialog.rowconfigure(1, weight=1)


        self.list_values = tk.StringVar()
        self.list_values2 = tk.StringVar()

        # FRAME
        frame_left = tk.Frame(self.popup_dialog)
        frame_left.grid(row=1, column=0, sticky='news')
        frame_right = tk.Frame(self.popup_dialog)
        frame_right.grid(row=1, column=1, sticky='news')

        # LABEL
        tk.Label(self.popup_dialog, text='TX messages').grid(row=0, column=0, sticky='w')
        tk.Label(self.popup_dialog, text='RX messages').grid(row=0, column=1, sticky='w')

        # LISTBOX
        self.pop_frame = tk.Listbox(frame_left, listvariable=self.list_values, height=5)
        self.pop_frame.pack(side=tk.LEFT, fill='both', expand=True)

        # SCROLBAR
        s = tk.Scrollbar(frame_left, orient=tk.VERTICAL, command=self.pop_frame.yview)
        s.pack(side=tk.RIGHT, fill=tk.Y)
        self.pop_frame.configure(yscrollcommand=s.set)

        # LISTBOX
        self.pop_frame2 = tk.Listbox(frame_right, listvariable=self.list_values2, height=5)
        self.pop_frame2.pack(side=tk.LEFT, fill='both', expand=True)

        # SCROLBAR
        s1 = tk.Scrollbar(frame_right, orient=tk.VERTICAL, command=self.pop_frame2.yview)
        s1.pack(side=tk.RIGHT, fill=tk.Y)

        self.pop_frame2.configure(yscrollcommand=s1.set)

        ttk.Sizegrip(self.popup_dialog).grid(row=2, column=1, stick='e')

        senders = self.dbc.nodes[index].tx
        receivers = self.dbc.nodes[index].rx
        self.list_values.set(senders)
        self.list_values2.set(receivers)

    def _close_popup(self):
        self.child.wm_attributes("-disabled", False)
        self.child.main.wm_attributes("-disabled", False)
        self.popup_dialog.destroy()

    def _button_add_dbc_to_list(self):
        dbc_file = self.txtSearch.get()
        if dbc_file != 'Chose the dbc file...' and dbc_file:
            for dbc in self.dbc_list:
                if dbc_file in dbc:
                    self.child.main.main_mesage_box('Selected a dbc file "{}" already in dbc list'.format(dbc_file))
                    return
            dbc = util.get_db_file(dbc_file, self.child)
            if dbc:
                index = self._get_dbc_list_index()
                self.dbc_list.append('{}: {}'.format(index, dbc_file))
                self.list_values.set(self.dbc_list)
                self.dbc = dbc
                self.current_dbc_index = index
                self._update_list_frame_ecu(self.child)
                self.list_box.selection_clear(0, tk.END)
                self.list_box.selection_set(tk.END, tk.END)
                self.txtSearch.set('Chose the dbc file...')
        else:
            self.child.main.main_mesage_box('Select a dbc file to be added to dbc list')

    def _get_dbc_list_index(self):
        if self.dbc_list:
            max = 0
            for item in self.dbc_list:
                item = item.split(':')
                if item[0].isdecimal():
                   if int(item[0]) > max:
                       max = int(item[0])
            return max + 1
        else:
            return 1

    def _button_search_dbc(self):
        dbc = self.child.open_dbc()
        self.txtSearch.set(dbc.get_dbc_full_name())

    def _button_clear_all(self):
        self.dbc_list = []
        self.ecus = []
        self.sel_items = []
        self.messages = {}
        self.current_dbc_index = 0

        self.txtSearch.set('Chose the dbc file...')
        self.dbc = []
        self.list_values.set(self.dbc_list)
        self._update_list_frame_ecu(self.child)
        self._update_selected_message()

    def _button_confirm(self):
        self.child.cnf['dbc_combine']['dbc_list'] = self.dbc_list.copy()
        self.child.cnf['dbc_combine']['ecus'] = self.ecus.copy()
        self.child.cnf['dbc_combine']['messages'] = self.messages.copy()
        self.child.on_modify_config()
        self._button_cancel()

    def _button_cancel(self):
        self.child.switch_frame(Config_frame.StartPage)
