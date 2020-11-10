import tkinter as tk
import const as Const
import frame_config as Config_frame, scrowframe as Scroll_Frame
import drawble as r


class ModifyList(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky='N,W,E,S')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # INITIALIZE VARIABLES
        self.child = child
        self.lbl_fig_lst = []  # label list_frame of items
        self.lbl_items_list = []  # label list_frame of items
        self.lbl_sel_item_lst = []  # label list_frame of selected items
        self.sel_items = {}  # list os selected items
        self.sel_item_id = 0  # last index of label_frame selected item
        self.searchIndex = 0  # index for consecutive seach
        self.totalItems = 0  # total items in the list

        self.autoset = tk.BooleanVar()  # autoset the message new values at each select to change on the list
        self.txtSearch = tk.StringVar()  #
        self.txtCycle = tk.StringVar()
        self.txtSize = tk.StringVar()

        self.autoset.set(True)
        self.txtSearch.set('Looking for...')
        self.txtCycle.set('100')
        self.txtSize.set('8')

        msg = ['Click in a message to select it to be modified',
               'The [Auto set values] checked will automatically modify the value of the message',
               'Click on a message in the Selected list to remove it',
               'The pencil icon means the message on DBC is selected to be modified']
        self.child.status_bar_list(msg)

        # IMAGES
        self.img = {
            Const.IMG_EDITED: tk.PhotoImage(file=r.IMG_PEN),
            Const.IMG_PLUS: tk.PhotoImage(file=r.IMG_PLUS),
            Const.IMG_EMPTY: tk.PhotoImage(file=r.IMG_GREY),
            Const.IMG_SEARCH: tk.PhotoImage(file=r.IMG_LUPA)
        }
        # self.img[Const.IMG_SEARCH].subsample(5,5)

        # LABEL
        tk.Label(self, text='DBC messages').grid(column=0, row=1, padx=(20, 0), pady=(2, 0), sticky='w')
        tk.Label(self, text='cycle time   msg size').grid(column=1, row=1, columnspan=3, pady=(2, 0), padx=(0, 35), sticky='e')
        tk.Label(self, text='Selected messages').grid(column=0, row=5, padx=(20, 0), pady=(12, 0), columnspan=2,
                                                      sticky='w')
        tk.Label(self, text='Cycle time (ms)').grid(column=0, row=4, padx=(20, 5), sticky='e')
        tk.Label(self, text='size (bytes)').grid(column=2, row=4, padx=(5, 5), sticky='e')

        # CHECKBOX
        tk.Checkbutton(self, text='Auto set values', variable=self.autoset,
                       onvalue=True, offvalue=False).grid(column=0, row=3, columnspan=5, padx=(20, 20), sticky='e')

        # ENTRY
        search = tk.Entry(self, textvariable=self.txtSearch)
        search.bind('<1>', lambda e: self._on_click_search())
        search.grid(column=1, row=0, columnspan=2, sticky='we')

        tk.Entry(self, width=4, textvariable=self.txtCycle).grid(column=1, row=4, sticky='we')
        tk.Entry(self, width=4, textvariable=self.txtSize).grid(column=3, row=4, padx=(0, 20), sticky='we')

        # VERTICAL_SCROLL_FRAME
        self._update_list_frame_msg(child)

        self._get_message_list()
        self._update_selected_message()

        # BUTTONS
        tk.Button(self, imag=self.img[Const.IMG_SEARCH],
                  command=lambda: self._button_search()) \
            .grid(column=3, row=0, padx=(2, 20), sticky='w')
        tk.Button(self, text="Clear list",
                  command=lambda: self._button_clear_list()) \
            .grid(column=2, row=8, columnspan=2, padx=(2, 20), pady=(2, 0), sticky='e')
        tk.Button(self, text="Cancel",
                  command=lambda: self._button_cancel()) \
            .grid(column=0, row=9, columnspan=2, padx=(20, 0), pady=(10, 5), sticky='w')
        tk.Button(self, text="Confirm",
                  command=lambda: self._button_confirm()) \
            .grid(column=2, row=9, columnspan=2, padx=(0, 20), pady=(10, 5), sticky='e')

    def _update_list_frame_msg(self, child):
        self.frame = Scroll_Frame.VerticalScrolledFrame(self, height=150, width=340, borderwidth=2, relief=tk.SUNKEN)
        self.frame.grid(column=0, row=2, columnspan=4, padx=20, sticky='nsew')

        for i in range(len(child.dbc.messages)):
            self.lbl_fig_lst.insert(i, [])
            self.lbl_items_list.insert(i, [])
            self.lbl_items_list[i] = tk.Label(self.frame, text=str(i) + ": " + child.dbc.messages[i].name)
            self.lbl_items_list[i].bind("<Button-1>", lambda e, index = i: self._on_click_item_label_frame(e, index))
            self.lbl_items_list[i].grid(column=1, row=i, sticky='W')

            tk.Label(self.frame, text=child.dbc.messages[i].cycle).grid(column=2, row=i, sticky='W')
            tk.Label(self.frame, text=child.dbc.messages[i].size).grid(column=3, row=i, sticky='W')

            if child.dbc.messages[i].name in child.cnf['modify_message'].keys():
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_EDITED])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_EDITED]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

            else:
                self.lbl_fig_lst[i] = tk.Label(self.frame, image=self.img[Const.IMG_EMPTY])
                self.lbl_fig_lst[i].image = self.img[Const.IMG_EMPTY]
                self.lbl_fig_lst[i].grid(column=0, row=i, sticky='nswe')

        self.totalItems = i

    def _get_message_list(self):
        self.sel_items = self.child.cnf['modify_message'].copy()

    def _update_selected_message(self):
        try:
            self.frame_selected.destroy()
        except:
            pass

        self.frame_selected = Scroll_Frame.VerticalScrolledFrame(self,
                                                                 height=100,
                                                                 width=300,
                                                                 borderwidth=2,
                                                                 relief=tk.GROOVE)
        self.frame_selected.grid(column=0, row=6, columnspan=4, sticky='nsew', padx=(20, 20))
        self.sel_item_id = 0
        for name, values in self.sel_items.items():
            self.lbl_sel_item_lst.insert(self.sel_item_id, [[], tk.StringVar(), tk.StringVar()])
            self.lbl_sel_item_lst[self.sel_item_id][0] = tk.Label(self.frame_selected, text="{:50}".format(name))
            self.lbl_sel_item_lst[self.sel_item_id][0].bind("<Button-1>",
                                                            lambda e: self._on_click_remove_item_label_frame())
            self.lbl_sel_item_lst[self.sel_item_id][0].grid(column=0, row=self.sel_item_id, sticky='w')
            tk.Entry(self.frame_selected, width=4,
                     textvariable=self.lbl_sel_item_lst[self.sel_item_id][1]).grid(column=2,
                                                                                   row=self.sel_item_id,
                                                                                   sticky='w')
            tk.Entry(self.frame_selected,
                     width=6,
                     textvariable=self.lbl_sel_item_lst[self.sel_item_id][2]).grid(column=1,
                                                                                   row=self.sel_item_id,
                                                                                   padx=5,
                                                                                   sticky='w')
            self.lbl_sel_item_lst[self.sel_item_id][1].set(values[0])
            self.lbl_sel_item_lst[self.sel_item_id][2].set(values[1])
            self.sel_item_id += 1

    def _add_selected_item(self, name, index):
        if self.autoset.get():
            size = self.txtSize.get()
            cycle = self.txtCycle.get()
        else:
            cycle, size = self._get_dbc_info(name)

        self.sel_items.update({name: [size, cycle]})
        self._update_selected_message()

    def _get_dbc_info(self, name):
        for msg in self.child.dbc:
            if msg.name == name:
                return [msg.cycle, msg.size]
        return ['8', '1000']

    def _remove_selected_item(self, nome):
        self.sel_items.pop(nome)
        self._update_selected_message()

    def _on_click_remove_item_label_frame(self):
        py = self.frame_selected.inner.winfo_pointery()
        outer_y = self.frame_selected.outer.winfo_y()
        index = (py - self.winfo_rooty() - outer_y - 7 - self.frame_selected.inner.winfo_y()) // 21
        m = self.lbl_sel_item_lst[index][0].cget('text').strip()
        self._empty_icon_in_list(m)
        self._remove_selected_item(m)

    def _empty_icon_in_list(self, item_name):
        self.lbl_fig_lst[self._looking_for_item(item_name)].config(image=self.img[Const.IMG_EMPTY])

    def _looking_for_item(self, name, type_search=True):
        for index in range(len(self.child.dbc.messages)):
            if type_search:
                if self.child.dbc.messages[index].name == name:
                    return index
            else:
                if name in self.child.dbc.messages[index].name:
                    if self.searchIndex < index:
                        self.searchIndex = index
                        return index
        self.searchIndex = 0  # item not found
        return 0

    def _on_click_item_label_frame(self, position, index):
        """py = self.frame.inner.winfo_pointery()
        index = (py - self.winfo_rooty() - self.frame.outer.winfo_y() - 7 - self.frame.inner.winfo_y()) // 21"""
        m = self.lbl_items_list[index].cget('text').split()
        m = m[1].strip()  # Get Message name without index number and spaces

        if m in self.sel_items:  # Remove from message list
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_EMPTY])
            self._remove_selected_item(m)
        else:  # Add to message list
            self.lbl_fig_lst[index].config(image=self.img[Const.IMG_EDITED])
            self._add_selected_item(m, index)

    def _on_click_search(self):
        if self.txtSearch.get() == 'Looking for...':
            self.txtSearch.set('')

    def _button_search(self):
        text = self.txtSearch.get().upper()
        if text != 'LOOKING FOR...' and text != "":
            position = self._looking_for_item(text, False)
            if position > 0:
                scroll = position / (self.totalItems - 6) * (
                            1 - (self.frame.canvas.yview()[1] - self.frame.canvas.yview()[0]))
                self.frame.canvas.yview_moveto(scroll)
                msg = "Item {} found in position {}".format(text, position)
            else:
                msg = "Item not found"
        else:
            msg = "Type your research first"
        self.child.status_bar_text(msg)

    def _button_clear_list(self):
        for msg in self.sel_items.keys():
            self._empty_icon_in_list(msg)
        self.sel_items.clear()
        self._update_selected_message()

    def _button_confirm(self):
        index = 0
        for k, v in self.sel_items.items():
            size = self.lbl_sel_item_lst[index][1].get()
            cycle = self.lbl_sel_item_lst[index][2].get()
            if len(size) == 0:
                size = '0'
            if len(cycle) == 0:
                cycle = '1000'
            self.sel_items[k][0] = size
            self.sel_items[k][1] = cycle
            index += 1

        self.child.cnf['modify_message'] = self.sel_items.copy()
        self.child.on_modify_config()
        self._button_cancel()

    def _button_cancel(self):
        self.child.switch_frame(Config_frame.StartPage)
