import tkinter as tk
from tkinter import ttk
import const as Const
import drawble as r
import util
import tutorial


class Splash(tk.Toplevel):
    def __init__(self, main, window_type=Const.WDW_SPLASH):
        self.img_list = []
        self.img_button = []

        if window_type == Const.WDW_WELCOME:
            self._mgmt_welcome()

        tk.Toplevel.__init__(self, main)
        self.iconbitmap(util.get_icon(r.ICO_HELP))
        self.wm_protocol("WM_DELETE_WINDOW", lambda: self._quit(main))
        self.minsize(300, 300)
        self.title(self._get_title(window_type))
        self.img_index = 0
        self.see_it_again = tk.StringVar()
        self.see_it_again.set(main.init_config.get('see_welcome'))
        self.fig = ''
        self.text = ''
        self.tutorial = ''

        if window_type == Const.WDW_WELCOME:
            self._frame_welcome()
        elif window_type == Const.WDW_ABOUT:
            self._mgmt_about()
        elif window_type == Const.WDW_TUTORIAL:
            self._mgmt_tutorial()

    def _mgmt_tutorial(self):
        self._frame_tutorial()
        self.tutorial = util.read_file('README.txt')
        if self.tutorial == '':
            self.tutorial = tutorial.tutorial
        for lines in self.tutorial:
            self.text.insert(tk.END, lines)

    def _mgmt_about(self):
        self._frame_about()

    def _mgmt_welcome(self):
        self._get_wecome_img_button()
        self._get_welcome_img()

    def _frame_about(self):
        # LABEL
        tk.Label(self, text='Licence: ' + Const.__copyright__).grid(row=0, column=0, padx=150, pady=30, stick='we')
        tk.Label(self, text='Version ' + Const.__version__)      .grid(row=1, column=0, padx=150, pady=10, stick='we')
        tk.Label(self, text='THIS SOFTWARE IS FOR FREE USAGE under ' + Const.__license__).grid(row=2, column=0, padx=150, pady=30, stick='we')
        tk.Label(self, text='by ' + Const.__author__) .grid(row=3, column=0, padx=150, pady=10, stick='we')
        tk.Label(self, text='email: ' + Const.__email__ ) .grid(row=4, column=0, padx=150, pady=30, stick='we')

    def _frame_tutorial(self):
        # CONFIGURE
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # TEXT
        self.text = tk.Text(self, width=60, height=20)
        self.text.grid(column=0, row=1, padx=(5,0), pady=5 , sticky="wnse")
        s2 = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        s2.grid(column=1, row=1, pady=5 , sticky="wns")
        self.text.configure(yscrollcommand=s2.set)

        # SIDEGRIP
        ttk.Sizegrip(self).grid(row=2, column=2, stick='e')

    def _frame_welcome(self):
        # BUTTON
        tk.Button(self, imag=self.img_button[Const.IMG_INDEX_LEFT],
                  command=lambda: self._button_welcome_left()) \
            .grid(row=0, column=0, padx=(5, 2), sticky='ns')
        tk.Button(self, imag=self.img_button[Const.IMG_INDEX_RIGHT],
                  command=lambda: self._button_welcome_right()) \
            .grid(row=0, column=2, padx=(2, 5), sticky='ns')

        # IMAGE
        self.fig = tk.Label(self, image=self.img_list[self.img_index])
        self.fig.image = self.img_list[self.img_index]
        self.fig.grid(column=1, row=0, sticky='nswe')

        # CHECKBUTTON
        chek = tk.Checkbutton(self, text='Do not see this window at startup', variable=self.see_it_again,
                              offvalue=False).grid(column=0, row=1, columnspan=2, sticky='w')

    def _get_welcome_img(self):
        self.img_list = util.get_welcome_images()

    def _get_wecome_img_button(self):
        self.img_button.append(util.get_image(r.IMG_LEFT))
        self.img_button.append(util.get_image(r.IMG_RIGTH))

    def _see_it(self):
        print(self.see_it_again.get())

    def _img_update(self):
        if self.img_index >= len(self.img_list):
            self.img_index = 0
        if self.img_index < 0:
            self.img_index = len(self.img_list) - 1
        self.fig.config(image=self.img_list[self.img_index])

    def _button_welcome_left(self):
        self.img_index -= 1
        self._img_update()

    def _button_welcome_right(self):
        self.img_index += 1
        self._img_update()

    def _get_title(self,window_type):
        return Const.WDW_TITLE[window_type]

    def _quit(self, main):
        main.init_config['see_welcome'] = self.see_it_again.get()
        self.destroy()