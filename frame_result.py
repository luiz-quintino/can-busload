import tkinter as tk
import drawble as r
import const as Const
import frame_config as Config_frame
import util


class ResultFrame(tk.Frame):
    def __init__(self, child):
        tk.Frame.__init__(self, child)

        self.grid(column=0, row=0, sticky=('N,W,E,S'))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # INITIALIZE VARIABLES
        msg = ['Busload Calc result']
        child.status_bar_list(msg)
        log = child.log
        calc = child.calc

        msg = ['Its possible to save the log in a .txt file',
               'The HTML is available in the Open recent report menu',
               'It is possible to compare several HTML report using Side-by-side report menu']
        child.status_bar_list(msg)

        # IMAGES
        self.img = {
            Const.IMG_PLUS: tk.PhotoImage(file=r.IMG_PLUS_B),
            Const.IMG_GARBAGE_RED: tk.PhotoImage(file=r.IMG_GARB_B),
            Const.IMG_GARBAGE_BLUE: tk.PhotoImage(file=r.IMG_GARB_RECYCLE_B),
            Const.IMG_EDITED: tk.PhotoImage(file=r.IMG_PEN_B),
            Const.IMG_DBC_COMBINE: tk.PhotoImage(file=r.IMG_COMBINE_B),
            Const.IMG_NOT: tk.PhotoImage(file=r.IMG_NOT_B),
        }

        # LABEL
        tk.Label(self, text='Calc result').grid(column=0, row=0, padx=(20, 0), pady=(12, 0), columnspan=2, sticky='w')

        # TEXT
        self.text = tk.Text(self, width=45, height=20)
        self.text.grid(column=0, row=1, columnspan=2, padx=(10, 0), pady=(5, 5), sticky="wnse")
        '''s1 = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        s1.grid(column=0, row=2, sticky=("wen"))
        self.text.configure(xscrollcommand=s1.set)'''
        s2 = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        s2.grid(column=2, row=1, padx=(0, 10), pady=(5, 5), sticky="wns")
        self.text.configure(yscrollcommand=s2.set)

        self._load_log(log, calc)
        self.text.config(state=tk.DISABLED)

        # BUTTONS
        if child.cnf.get('csv').lower() == 'true':
            tk.Button(self, text="Open csv report",
                      command=lambda: self._button_open_csv(child)) \
                .grid(column=0, row=3, padx=(20,0), pady=(10, 0), sticky='w')
        if child.cnf.get('html').lower() == 'true':
            tk.Button(self, text="Open html report",
                      command=lambda: self._button_open_html_report(child)) \
                .grid(column=1, row=3, padx=(0, 20), pady=(10, 0), sticky='e')
        tk.Button(self, text="Save log", width=10,
                  command=lambda: self._button_save_log()) \
            .grid(column=0, row=4, columnspan=2, padx=(0, 20), pady=(10, 0), sticky='e')
        tk.Button(self, text="Back", width=10,
                  command=lambda: self._button_cancel(child)) \
            .grid(column=0, row=4, columnspan=2, padx=(20, 0), pady=(10, 0), sticky='w')

    def _button_open_html_report(self, child):
        child.open_last_html()

    def _button_open_csv(self, child):
        child.open_last_csv()

    def _load_log(self, log, result):
        self.text.insert(tk.END, "Busload log\n  ")
        self.text.insert(tk.END, "\n*******************************\n")
        self.text.insert(tk.END, "Applying configuration....\n")
        self.text.insert(tk.END, "*******************************\n")
        for rs in log:
            txt = rs.split(":")
            if len(txt) > 1:
                if '[r]' in txt[0]:
                    self.text.window_create(tk.END, window=tk.Label(self.text, image=self.img[Const.IMG_GARBAGE_RED]))
                elif '[m]' in txt[0]:
                    self.text.window_create(tk.END, window=tk.Label(self.text, image=self.img[Const.IMG_EDITED]))
                elif '[n]' in txt[0]:
                    self.text.window_create(tk.END, window=tk.Label(self.text, image=self.img[Const.IMG_NOT]))
                elif '[+]' in txt[0]:
                    self.text.window_create(tk.END, window=tk.Label(self.text, image=self.img[Const.IMG_PLUS]))
                elif '[c]' in txt[0]:
                    self.text.window_create(tk.END, window=tk.Label(self.text, image=self.img[Const.IMG_DBC_COMBINE]))
                else:
                    self.text.insert(tk.END, txt[0] + ":")

                self.text.insert(tk.END, " " + txt[1])
            else:
                self.text.insert(tk.END, txt[0])

            self.text.insert(tk.END, "\n")

        self.text.insert(tk.END, "\n*******************************\n")
        self.text.insert(tk.END, "Messages used to calc....\n")
        self.text.insert(tk.END, "*******************************\n")
        self.text.insert(tk.END, "{:25} {:6} {:6}\n".format('message name', 'msg time', 'msg load'))

        for rs in result[0]:
            self.text.insert(tk.END, "{:25} {:0.6f} {:0.6f}\n".format(rs.name[:19], rs.messagetime, rs.messageload))

        self.text.insert(tk.END, "\n*******************************\n")
        self.text.insert(tk.END, "Messages not used to calc....\n")
        self.text.insert(tk.END, "*******************************\n")
        self.text.insert(tk.END, "{:25} {:6}\n".format('message name', 'cycle time'))
        for rs in result[1]:
            self.text.insert(tk.END, "{:25} {:0.6f}\n".format(rs.name[:19], rs.cycle))

    def _button_save_log(self):
        util.save_log(self.text.get(0.1, tk.END))

    def _button_cancel(self, child):
        child.switch_frame(Config_frame.StartPage)
