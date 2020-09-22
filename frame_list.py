import tkinter as tk
from tkinter import ttk
import const as Const
import frame_config as Config_frame, scrowframe as Scroll_frame
import drawble as r
import util


class EraseList(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # INITIALIZE VARIABLES
        self.child = child
        self.lbl_fig_lst = []  # label list_frame of items
        self.lbl_items_list = []  # label list_frame of items
        self.lbl_sel_item_lst = []  # label list_frame of selected items
        self.sel_items = []  # list os selected items
        self.sel_item_id = 0  # last index of label_frame selected item
        self.searchIndex = 0  # index for consecutive seach
        self.totalItems = 0  # total items in the list
        self.frameConf = child.frm_conf  # define the frame behavior: ecu or msg

        # IMAGES
        self.img = {
            Const.IMG_GARBAGE_EMPTY: util.get_image(r.IMG_GARB_EMPTY),
            Const.IMG_GARBAGE_RED: util.get_image(r.IMG_GARB_RED),
            Const.IMG_GARBAGE_BLUE: util.get_image(r.IMG_GARB_BLUE),
            Const.IMG_SEARCH: util.get_image(r.IMG_LUPA)
        }
        # self.img[Const.IMG_SEARCH].subsample(5,5)

        # LABEL
        tk.Label(self, text=Const.SUB_FRAME[child.frm_conf]['lbl_frame']).grid(column=0, row=1, padx=20, pady=(2, 0),
                                                                               sticky='w')
        tk.Label(self, text=Const.SUB_FRAME[child.frm_conf]['lbl_sel']).grid(column=0, row=3, padx=20, pady=(12, 0),
                                                                             columnspan=2, sticky='w')

        if self.frameConf == Const.SB_ERASE_MGS:
            tk.Label(self, text='cycle time   msg size').grid(column=1, row=1, columnspan=3, pady=(2, 0), padx=(0, 35),
                                                          sticky='e')

        # ENTRY
        self.txtSearch = tk.StringVar()
        self.txtSearch.set('Looking for...')
        search = tk.Entry(self, textvariable=self.txtSearch)
        search.bind('<1>', lambda e: self._on_click_search())
        search.grid(column=1, row=0, sticky='we')

        # VERTICAL_SCROLL_FRAME
        self.frame = Scroll_frame.VerticalScrolledFrame(self, height=200, width=340, borderwidth=2, relief=tk.SUNKEN)
        self.frame.grid(column=0, row=2, columnspan=3, padx=20, sticky='nsew')

        if self.frameConf == Const.SB_ERASE_ECU:
            self._update_list_frame_ecu(child)
            msg = ['Click on the ECU in the list to select it to delete',
                   'Click on the selected ECU to remove it from the list',
                   'Blue garbage means only message sent by that module will be deleted'
                   'Red garbage or "*" means all messages from that module will be deleted',
                   'Use right mouse button to see the list of messages sent by the ECU']
        else:
            self._update_list_frame_msg(child)
            msg = ['Click on the Message in the list to select it to delete',
                   'Click on the selected Message to remove it from the list',
                   'Use right mouse button to see the list of ECU senders for that message']

        self._update_selected_message()
        self.child.status_bar_list(msg)

        # BUTTONS
        tk.Button(self, imag=self.img[Const.IMG_SEARCH],
                  command=lambda: self._button_search()) \
            .grid(column=2, row=0, columnspan=2, padx=(2, 20), sticky='w')
        tk.Button(self, text="Clear list",
                  command=lambda: self._button_clear_list()) \
            .grid(column=1, row=5, columnspan=2, padx=(2, 20), pady=(2, 0), sticky='e')
        tk.Button(self, text="Cancel",
                  command=lambda: self._button_cancel()) \
            .grid(column=0, row=6, columnspan=3, padx=20, pady=(10, 5), sticky='w')
        tk.Button(self, text="Confirm",
                  command=lambda: self._button_confirm()) \
            .grid(column=0, row=6, columnspan=3, padx=20, pady=(10, 5), sticky='e')

    def _update_list_frame_msg(self, child):
        self.frame = Scroll_frame.VerticalScrolledFrame(self, height=200, width=340, borderwidth=2, relief=tk.SUNKEN)
        self.frame.grid(column=0, row=2, columnspan=3, padx=20, sticky='nsew')

        for i in range(len(child.dbc.messages)):
            self.lbl_fig_lst.insert(i, [])
            self.lbl_items_list.insert(i, [])
            self.lbl_items_list[i] = tk.Label(self.frame, text=str(i) + ": " + child.dbc.messages[i].name)
            self.lbl_items_list[i].bind("<Button-1>", lambda e, cv=i: self._on_click_item_label_frame(e, cv))
            self.lbl_items_list[i].bind("<Button-3>", lambda a, b=i: self._on_left_click_item_label_frame(a, b))
            self.lbl_items_list[i].grid(column=1, row=i, sticky='W')

            tk.Label(self.frame, text=child.dbc.messages[i].cycle).grid(column=2, row=i, sticky='W')
            tk.Label(self.frame, text=child.dbc.messages[i].size).grid(column=3, row=i, sticky='W')

            if child.dbc.messages[i].name in child.cnf['erase_message']:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_GARBAGE_RED])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_GARBAGE_RED]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

                # create list of messages selected
                self.sel_items.append(child.dbc.messages[i].name)
            else:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_GARBAGE_EMPTY])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_GARBAGE_EMPTY]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

        self.totalItems = i

    def _update_list_frame_ecu(self, child):

        self.frame = Scroll_frame.VerticalScrolledFrame(self, height=200, width=340, borderwidth=2, relief=tk.SUNKEN)
        self.frame.grid(column=0, row=2, columnspan=3, padx=20, sticky='nsew')

        for i in range(len(child.dbc.nodes)):
            self.lbl_fig_lst.insert(i, [])
            self.lbl_items_list.insert(i, [])
            self.lbl_items_list[i] = tk.Label(self.frame, text=str(i) + ": " + child.dbc.nodes[i].name)
            self.lbl_items_list[i].bind("<Button-1>", lambda e, cv=i: self._on_click_item_label_frame(e, cv))
            self.lbl_items_list[i].bind("<Button-3>", lambda a, b=i: self._on_left_click_item_label_frame(a, b))
            self.lbl_items_list[i].grid(column=1, row=i, sticky='W')

            if child.dbc.nodes[i].name + '*' in child.cnf['erase_ecu']:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_GARBAGE_BLUE])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_GARBAGE_BLUE]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')
                # create list of messages selected
                self.sel_items.append(child.dbc.nodes[i].name + '*')
            elif child.dbc.nodes[i].name in child.cnf['erase_ecu']:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_GARBAGE_RED])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_GARBAGE_RED]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')
                # create list of messages selected
                self.sel_items.append(child.dbc.nodes[i].name)
            else:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_GARBAGE_EMPTY])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_GARBAGE_EMPTY]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

        self.totalItems = i

    def _update_selected_message(self):
        try:
            self.frame_selected_items.destroy()
        except Exception as e:
            pass

        self.frame_selected_items = Scroll_frame.VerticalScrolledFrame(self, height=100, width=300,
                                                                       borderwidth=2, relief=tk.GROOVE)
        self.frame_selected_items.grid(column=0, row=4, columnspan=3, sticky='nsew', padx=(20, 20))
        self.sel_item_id = 0
        for name in self.sel_items:
            self.lbl_sel_item_lst.insert(self.sel_item_id, [])
            self.lbl_sel_item_lst[self.sel_item_id] = tk.Label(self.frame_selected_items, text=name)
            self.lbl_sel_item_lst[self.sel_item_id].bind("<Button-1>",
                                                         lambda e, cv = self.sel_item_id: self._on_click_remove_item_label_frame(e, cv))
            self.lbl_sel_item_lst[self.sel_item_id].grid(column=1, row=self.sel_item_id, sticky='w')
            self.sel_item_id += 1

    def _add_selected_item(self, name):
        self.sel_items.append(name)
        self._update_selected_message()

    def _remove_selected_item(self, nome):
        self.sel_items.remove(nome)
        self._update_selected_message()

    def _empty_icon_in_list(self, item_name):
        self.lbl_fig_lst[self._looking_for_item(item_name)].config(image=self.img[Const.IMG_GARBAGE_EMPTY])

    def _looking_for_item(self, name, search_type=True):
        # search_type True = search by name, False = search in a list of names
        if self.frameConf == Const.SB_ERASE_MGS:
            for index in range(len(self.child.dbc.messages)):
                if search_type:
                    if self.child.dbc.messages[index].name == name:
                        return index
                else:
                    if name in self.child.dbc.messages[index].name:
                        if self.searchIndex < index:
                            self.searchIndex = index
                            return index
        else:
            for index in range(len(self.child.dbc.nodes)):
                if search_type:
                    if self.child.dbc.nodes[index].name == name:
                        return index
                else:
                    if name in self.child.dbc.nodes[index].name:
                        if self.searchIndex < index:
                            self.searchIndex = index
                            return index

        self.searchIndex = 0  # item not found
        return 0

    def _on_click_remove_item_label_frame(self, position, index):
        """p_inner_pointer_y = self.frame_selected_items.inner.winfo_pointery()
        p_inner_outer_y = self.frame_selected_items.outer.winfo_y()
        p_inner_y = self.frame_selected_items.inner.winfo_y()
        index = (p_inner_pointer_y - self.winfo_rooty() - p_inner_outer_y - 7 - p_inner_y) // 21"""
        m = self.lbl_sel_item_lst[index].cget('text')
        if m[-1] == '*':
            self._empty_icon_in_list(m[:-1])
        else:
            self._empty_icon_in_list(m)
        self._remove_selected_item(m)

    def _on_click_item_label_frame(self, positon, index):
        """Obsolete: py = self.frame.inner.winfo_pointery()
        index = (py - self.winfo_rooty() - self.frame.outer.winfo_y() - 7 - self.frame.inner.winfo_y()) // 21"""
        m = self.lbl_items_list[index].cget('text').split()
        m = m[1].strip()  # Get Message name without index number and spaces
        if m in self.sel_items:     # Remove Message or put * in ECU from the 'selected list'
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_GARBAGE_EMPTY])
            self._remove_selected_item(m)
            if self.frameConf == Const.SB_ERASE_ECU:
                self.lbl_fig_lst[index].config(image=self.img[Const.IMG_GARBAGE_RED])
                self._add_selected_item(m + '*')
        elif m + '*' in self.sel_items:               # Remove ECU from the 'selected list'
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_GARBAGE_EMPTY])
            self._remove_selected_item(m + '*')
        else:                                   # Messege/ECU not found, ADD it to 'selected list'
            if self.frameConf == Const.SB_ERASE_MGS:
                self.lbl_fig_lst[index].config(image=self.img[Const.IMG_GARBAGE_RED])
            else:
                self.lbl_fig_lst[index].config(image=self.img[Const.IMG_GARBAGE_BLUE])
            self._add_selected_item(m)

    def _on_click_search(self):
        if self.txtSearch.get() == 'Looking for...':
            self.txtSearch.set('')

    def _on_left_click_item_label_frame(self, position, index):
        x = self.frame.inner.winfo_pointerx()
        y = self.frame.inner.winfo_pointery()
        self._popup_window(x, y, index)

    def _popup_window(self, x, y, index):
        # THE CLUE
        self.child.wm_attributes("-disabled", True)
        self.child.main.wm_attributes("-disabled", True)

        if self.frameConf == Const.SB_ERASE_MGS:
            title = 'Senders: {}'.format(self.child.dbc.messages[index].name)
        else:
            title = 'Msg list: {}'.format(self.child.dbc.nodes[index].name)

        # Creating the toplevel dialog
        self.popup_dialog = tk.Toplevel(self.child)
        self.popup_dialog.title(title)
        self.popup_dialog.geometry('200x200+{}+{}'.format(x, y))
        self.popup_dialog.minsize(200, 200)
        self.popup_dialog.transient(self.child)
        self.popup_dialog.protocol("WM_DELETE_WINDOW", self._close_popup)
        self.popup_dialog.iconbitmap(r.ICO_CHILD)

        self.list_values = tk.StringVar()
        self.pop_frame = tk.Listbox(self.popup_dialog, listvariable=self.list_values, height=5)
        self.pop_frame.pack(side=tk.LEFT,fill='both', expand=True)

        # SCROLBAR
        s = tk.Scrollbar(self.popup_dialog, orient=tk.VERTICAL, command=self.pop_frame.yview)
        s.pack(side=tk.RIGHT, fill=tk.Y)
        self.pop_frame.configure(yscrollcommand=s.set)

        ttk.Sizegrip(s).pack(side=tk.BOTTOM)

        list = []
        if self.frameConf == Const.SB_ERASE_MGS:
            for msg in self.child.dbc.messages[index].senders:
                list.append(msg)
        else:
            ecu = self.child.dbc.nodes[index].name
            for msg in self.child.dbc.messages:
                if ecu in msg.senders:
                    list.append(msg.name)
        self.list_values.set(list)

    def _close_popup(self):
        self.child.wm_attributes("-disabled", False)
        self.child.main.wm_attributes("-disabled", False)
        self.popup_dialog.destroy()

    def _button_search(self):
        text = self.txtSearch.get().upper()
        if text != 'LOOKING FOR...' and text != "":
            pst = self._looking_for_item(text, False)
            if pst > 0:
                scroll = pst / (self.totalItems - 8) * (
                        1 - (self.frame.canvas.yview()[1] - self.frame.canvas.yview()[0]))
                self.frame.canvas.yview_moveto(scroll)
                msg = "Item {} found in position {}".format(text, pst)
            else:
                msg = "Item not found"
        else:
            msg = "Type your research first"

        self.child.status_bar_text(msg)

    def _button_clear_list(self):
        for msg in self.sel_items:
            if msg[-1] == '*':
                msg = msg[:-1]
            self._empty_icon_in_list(msg)
        self.sel_items = []
        self._update_selected_message()

    def _button_confirm(self):
        if self.frameConf == Const.SB_ERASE_MGS:
            self.child.cnf['erase_message'] = self.sel_items.copy()
        else:
            self.child.cnf['erase_ecu'] = self.sel_items.copy()
        self.child.on_modify_config()
        self._button_cancel()

    def _button_cancel(self):
        self.child.switch_frame(Config_frame.StartPage)
