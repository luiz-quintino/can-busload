import tkinter as tk
import drawble as r
import const as Const
import util
import os
from tkinter import ttk


class SideWindow(tk.Toplevel):
    def __init__(self, main, my_id):
        tk.Toplevel.__init__(self, main)
        self.geometry('400x380' + main.get_child_window_position())
        self.iconbitmap(util.get_icon(r.ICO_SIDE))
        self.wm_protocol("WM_DELETE_WINDOW", lambda: self.quit())
        self.minsize(350, 300)
        self.maxsize(main.winfo_width() - 30, main.winfo_height() - 70)
        self.transient(main)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        #self.columnconfigure(4, weight=1)
        self.title('Side-by-side comparision')
        self.bind('<Configure>', main.state_child)


        self.saved = True
        self.main = main
        self.report_list = {}
        self.valid_file_list(self.get_file_list())
        self.output_name = tk.StringVar()

        # Loop of status bar messages
        msg = ['Select at least one HTML report to generate the side-by-side',
               'Write a new to side-by-side file or select the auto generate',
               'Only valid HTML report is presented in the list']
        self.main.status_bar.set_list(msg)

        # LABEL
        tk.Label(self, text='Select the html reports to a side by side comparison')\
            .grid(row=1, column=0, columnspan=4, padx=10, pady=5, stick='w')
        tk.Label(self, text='Side-by-side file name')\
            .grid(row=0, column=0, columnspan=2, pady=5, padx=2, stick='e')

        # ENTRY
        tk.Entry(self, textvariable=self.output_name) \
            .grid(row=0, column=2, columnspan=2, pady=5, stick='we')

        # BUTTON
        self.img = util.get_image(r.IMG_SPARK) #tk.PhotoImage(file=r.IMG_SPARK)
        tk.Button(self, imag=self.img,
                  command=lambda: self._get_title(main)) \
            .grid(row=0, column=4, padx=(0, 10), sticky='w')

        # LISBOX
        self.list_values = tk.StringVar()
        self.list_box = tk.Listbox(self, listvariable=self.list_values, height=5, selectmode=tk.MULTIPLE)
        self.list_box.grid(row=2, column=0, columnspan=4, padx=(10,0), stick='news')

        # SCROLBAR
        s = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.list_box.yview)
        s.grid(row=2, column=4, padx=(0,5), stick='ns')
        self.list_box.configure(yscrollcommand=s.set)

        # BUTTONS
        tk.Button(self, text='Clear selection', command=self.button_clear_selection)\
            .grid(row=3, column=0, padx=(10,2), pady=10, stick='we')
        tk.Button(self, text='Select all', command=self.button_list_select_all)\
            .grid(row=3, column=1, padx=2, pady=10, stick='we')
        tk.Button(self, text='Side by side report', command=self.button_report)\
            .grid(row=3, column=2, padx=2, pady=10, stick='we')
        tk.Button(self,text='Close', command=self.quit)\
            .grid(row=3, column=3, padx=2, pady=10, stick='we')

        # SIDEGRIP
        ttk.Sizegrip(self).grid(row=4, column=4, stick='e')

        list = [ k for k in self.report_list.keys()]
        list.sort()
        self.list_values.set(list)

    def _get_title(self, main):
        index = main.init_config.get('index_side_title') + 1
        if index > 999:
            index = 0
        main.init_config['index_side_title'] = index
        self.output_name.set("New_side_by_syde_{:03d}".format(index))

    def button_report(self):
        selected_text_list = [self.list_box.get(i) for i in self.list_box.curselection()]
        name = self.output_name.get().strip()
        if name:
            output_file = 'output/sbs/' + name + '.html'

            if os.path.exists(output_file):
                answer = self.main.main_mesage_box('File "{}" already exists.\nOverwrite it\n'.format(output_file)
                                                   ,Const.MSG_YES_NO)
                if not answer:
                    return
            if selected_text_list:
                result = util.save_side_report_html(output_file, selected_text_list, self.report_list)
                if result == True:
                    self.main.open_html(output_file)
                    self.main.add_recent_side(output_file)
                else:
                    self.main.main_mesage_box('Error writing side_by_side report.\n{}'.format(result))
            else:
                self.main.main_mesage_box('Select at least one file to compare')
        else:
            self.main.main_mesage_box('File name required to side_by_side report')

    def button_clear_selection(self):
        self.list_box.selection_clear(0, tk.END)

    def button_list_select_all(self):
        self.list_box.selection_set(0, tk.END)

    def valid_file_list(self, file_list):
        for file in file_list:
            if '.html' in file:
                content = util.read_file('output/' + file)
                self.read_meta_data(content, file)

    def read_meta_data(self, data, file):
        data = ''.join(data)
        if 'result@busloadcalc' in data:
            start = data.index('result@busloadcalc')
            beguin = data.index('"', start) + 1
            end = data.index('"', beguin)
            my_data = data[beguin:end].split(',')
            if len(my_data) > 3:
                # Configuration Report version 2.1
                if my_data[0].strip() == 'Busload Calc configuration' and my_data[3].strip() == '2.1':
                    my_dict = {my_data[i].strip(): my_data[i + 1].strip() for i in range(0, len(my_data), 2)}
                    self.report_list.update({file: my_dict})

    def get_file_list(self):
        if os.path.isdir('output'):
            return os.listdir('output/')

    def quit(self):
        self.main.side_is_open = False
        self.main.quit_child(self.winfo_id())