import tkinter as tk
import const as Const
import window_child as Child_window
import window_side
import window_splash
import drawble as r
import util
from config import Config
from tkinter import messagebox
from tkinter import filedialog
from file_name import FileName
import os
import webbrowser
import winsound


class Main(tk.Tk):
    def __init__(self):
        # CREATE MAIN WINDOW
        tk.Tk.__init__(self)
        self.title("Busload Calc 2.1")
        self.option_add('*tearOff', False)
        self.geometry('900x600')
        self.minsize(480, 600)
        self.iconbitmap(util.get_icon(r.ICO_MAIN))
        self.wm_protocol("WM_DELETE_WINDOW", lambda: self.quit())

        # CREATE MAIN MENU OBJECT
        self.menu = CreateMenu(self)

        # CREATE STATUS BAR
        self.status_bar = StatusBar(self)

        # SET GLOBAL PARAMETERS
        self.pos = []  # main window position
        self.init_position = 0  # initial position for new child window
        self.child_windows = []  # list of child windows
        self.configs = []  # list of configurations
        self.init_config = []
        self.side_is_open = False

        self.default_status_bar_message()

        self._apply_file_init()
        self.status_bar.responsible.set(self.init_config.get('responsible'))

        if self.init_config.get('see_welcome') == '0':
            self.open_welcome_window()

    def _apply_file_init(self):
        config = util.reading_json(Const.BUSLOAD_INIT, self)
        if not self._is_valide_init_config(config):
            config = self._get_default_init()

        self.init_config = config
        config = self._check_file_name(self.init_config['recent_config'])
        report = self._check_file_name(self.init_config['recent_report'])
        side = self._check_file_name(self.init_config['recent_side'])
        self.menu.recent_menu_update_config(config, self)
        self.menu.recent_menu_update_report(report, self)
        self.menu.recent_menu_update_side(side, self)

    def _check_file_name(self, file_list):
        return [file for file in file_list if os.path.exists(file)]

    def _is_valide_init_config(self, config):
        if config:
            if 'version' in config.keys():
                if config['version'] == "2.1":
                    return True
        return False

    def _get_default_init(self):
        if not os.path.exists('dbc'):
            os.mkdir('dbc')
        if not os.path.exists('configs'):
            os.mkdir('configs')
        if not os.path.exists('output'):
            os.mkdir('output')

        config = {
            "Busload Calc configuration": "2020",
            "version": "2.1",
            "responsible": "@Responsible name",
            "index_title": 0,
            "index_side_title": 0,
            "max_recent": 20,
            "see_welcome": "0",
            "yellow_region": "50",
            "red_region": "70",
            "recent_side": [],
            "recent_config": [],
            "recent_report": []
        }
        self.main_mesage_box ('File "{}" created successfully.'.format(Const.BUSLOAD_INIT))
        return config

    def add_recent_config(self, file):
        if file and file not in self.init_config['recent_config']:
            self.menu.recent_menu_update_config([file], self)
            if len(self.init_config['recent_config']) > self.init_config['max_recent']:
                self.init_config['recent_config'].pop(0)
                self.menu.remove_config()
            self.init_config['recent_config'].append(file)

    def add_recent_side(self, file):
        if file and file not in self.init_config['recent_side']:
            self.menu.recent_menu_update_side([file], self)
            if len(self.init_config['recent_side']) > self.init_config['max_recent']:
                self.init_config['recent_side'].pop(0)
                self.menu.remove_side()
            self.init_config['recent_side'].append(file)

    def add_recent_report(self, file):
        if file and file not in self.init_config['recent_report']:
            self.menu.recent_menu_update_report([file], self)
            if len(self.init_config['recent_report']) > self.init_config['max_recent']:
                self.init_config['recent_report'].pop(0)
                self.menu.remove_report()
            self.init_config['recent_report'].append(file)

    def run_calc(self, config):
        util.apply_config(config)
        self.status_bar.set_status_msg('Calculating Busload...')
        config.yellow = self._define_region(self.init_config.get('yellow_region'))
        config.red =self._define_region(self.init_config.get('red_region'))

        try:
            util.calc_busload(config)
            return config
        except Exception as e:
            self.main_mesage_box('Error during busload calculation. \nDBC format not supported.\n\n{}'.format(e))
            return []

    def _define_region(self, value):
        try:
            result = int(value) * 2 + 110
        except:
            result = 210
        return result

    def get_child_window_position(self):
        x, y = self.winfo_rootx() + self.init_position, self.winfo_rooty() + (self.init_position % 50)
        self.init_position += 20
        return '+{}+{}'.format(x, y)

    def open_side_by_side_window(self):
        if not self.side_is_open:
            self.side_is_open = True
            self.child_windows.append(window_side.SideWindow(self, len(self.child_windows)))
            self.bind('<Configure>', self.state_main)

    def config_status_to_calc(self, turn_on=True):
        if turn_on:
            self.status_bar.set_timeout_off()
        else:
            self.status_bar.set_timeout_on()

    def default_status_bar_message(self):
        self.status_bar.set_list(['Start a new configuration on New Config menu',
                                  'Open an existing configuration on Open Config menu',
                                  'Put your name on the Responsible status bar to auto fulfill the New config'
                                  'Busload Calc 2.0'])

    def menu_new_config(self):
        self.configs.append(Config())
        self.child_windows.insert(-1, Child_window.Child(self, self.configs[-1]))
        self.bind('<Configure>', self.state_main)

    def menu_save_as(self, title):
        if not title.file_extension:
            title.file_extension = '.cnf'
        file = filedialog.asksaveasfilename(initialdir="configs/", initialfile=title.file_name + title.file_extension,
                                            title="Save as a configuration file",
                                            filetypes=[("Busload config", "*.cnf")])
        title = FileName(file)
        if not title.file_extension:
            title.file_extension = '.cnf'
        return title

    def _is_config_already_open(self, title):
        for child in self.child_windows:
            short_name = title.lower().split('/')
            short_name = short_name[-1].split('.')
            if child.title() == short_name[-2]:
                return True
        return False

    def open_welcome_window(self):
        self.welcome = window_splash.Splash(self, Const.WDW_WELCOME)

    def open_about_window(self):
        self.welcome = window_splash.Splash(self, Const.WDW_ABOUT)

    def open_tutorial_window(self):
        self.welcome = window_splash.Splash(self, Const.WDW_TUTORIAL)

    def open_duplicated_config(self, config):
        self.configs.append(Config())
        self.configs[-1].cnf = config
        self.configs[-1].config_name = ""
        self.child_windows.append(Child_window.Child(self,
                                                     self.configs[-1]))

    def open_config(self, title):
        if os.path.exists(title):
            if not self._is_config_already_open(title):
                self.configs.append(Config())
                self.configs[-1].config_name = FileName(title)
                self.child_windows.append(Child_window.Child(self,
                                                             self.configs[-1],
                                                             self.configs[-1].config_name.file_name))
                self.bind('<Configure>', self.state_main)
                self.add_recent_config(title)
            else:
                self.main_mesage_box('File "{}" already open.'.format(title))
        else:
            self.main_mesage_box('File "{}" not found.'.format(title), Const.MSG_ERROR)

    def open_html(self, file):
        try:
            webbrowser.open('file://' + os.path.realpath(file))
        except Exception as e:
            self.main_mesage_box('Error opening {}\n{}'.format(file, e))

    def open_csv(self, file):
        file_name = ''
        for char in file:
            if char == '/':
                file_name += '\\'
            else:
                file_name += char
        try:
            os.startfile(file_name)
        except Exception as e:
            self.main_mesage_box('Error opening {}\n{}'.format(file_name, e))

    def menu_open_dbc(self):
        title = filedialog.askopenfilename(initialdir="dbc/",
                                           title="Select dbc file",
                                           filetypes=[("Busload config", "*.dbc")])
        return FileName(title)

    def menu_open_config(self):
        title = filedialog.askopenfilename(initialdir="configs/",
                                           title="Select configuration file",
                                           filetypes=[("Busload config", "*.cnf")])

        if title:
            title = FileName(title)
            self.open_config(title.get_full_name())

    def state_main(self, *args):
        if self.pos:
            dx = self.pos[0] - self.winfo_x()
            dy = self.pos[1] - self.winfo_y()
            wd = self.winfo_width()
            he = self.winfo_height()
            for c in self.child_windows:
                cwd = c.winfo_width()
                che = c.winfo_height()
                cwd = cwd if cwd + 30 < wd else wd - 30
                che = che if che + 70 < he else he - 70
                c.geometry("{}x{}+{}+{}".format(cwd, che, c.winfo_x() - dx, c.winfo_y() - dy))

        self.pos = [self.winfo_x(), self.winfo_y()]

    def state_child(self, event, *args):
        min_w = self.winfo_rootx()
        min_h = self.winfo_rooty()
        max_w = self.winfo_rootx() + self.winfo_width() - 10
        max_h = self.winfo_rooty() + self.winfo_height() - 65

        for child_window in self.child_windows:
            if child_window.winfo_x() < min_w:
                child_window.geometry("+{0}+{1}".format(min_w, event.y))
                # app.event_generate('<Motion>', warp=True, x = pos[2] + 1, y = pos[3] + pos[5])
            if child_window.winfo_y() < min_h:
                child_window.geometry("+{0}+{1}".format(event.x, min_h))
            if child_window.winfo_x() + child_window.winfo_width() > max_w:
                child_window.geometry("+{0}+{1}".format(max_w - event.width, event.y))
            if child_window.winfo_y() + child_window.winfo_height() > max_h:
                child_window.geometry("+{0}+{1}".format(event.x, max_h - event.height))

    def quit_child(self, child_id, *args):
        for i in range(len(self.child_windows)):
            if child_id == self.child_windows[i].winfo_id():
                self.child_windows[i].destroy()
                del self.child_windows[i]
                if len(self.child_windows) == 0:
                    self.unbind('<Configure>')
                    self.default_status_bar_message()
                break

    def quit(self, *args):
        for child in self.child_windows:
            if not child.saved:
                child.ask_to_save()

        util.writing_json(self.init_config, Const.BUSLOAD_INIT, self)
        self.destroy()

    def main_mesage_box(self, message, box_type=Const.MSG_INFO):
        winsound.Beep(5800, 50)
        if box_type == Const.MSG_INFO:
            return messagebox.showinfo("Attention", message)
        if box_type == Const.MSG_ERROR:
            return messagebox.showerror("Error", message)
        if box_type == Const.MSG_QUESTION:
            return messagebox.askquestion("Buload Calc", message)
        if box_type == Const.MSG_WARNING:
            return messagebox.showwarning("Warning", message)
        if box_type == Const.MSG_OK_CANCEL:
            return messagebox.askokcancel("Busload Calc", message)
        if box_type == Const.MSG_YES_NO:
            return messagebox.askyesno("Busload Calc", message)
        if box_type == Const.MSG_RETRY:
            return messagebox.askretrycancel("Retry", message)


class CreateMenu(tk.Menu):
    def __init__(self, main):
        tk.Menu.__init__(self, main)

        self.main_menu = self
        self.menu_open = tk.Menu(self)
        self.menu_recent_report = tk.Menu(self)
        self.menu_recent_config = tk.Menu(self)
        self.menu_report = tk.Menu(self)
        self.menu_recent_side = tk.Menu(self)
        self.menu_help = tk.Menu(self)

        # MAIN MENU OPTIONS
        self.main_menu.add_cascade(label="Open", menu=self.menu_open)
        self.main_menu.add_command(label="Side-by-side report", command=main.open_side_by_side_window)
        self.main_menu.add_cascade(label="Open recent report", menu=self.menu_report)
        self.main_menu.add_cascade(label="Help", menu=self.menu_help)
        self.main_menu.add_command(label="Exit", command=main.quit)

        # OPEN OPTIONS
        self.menu_open.add_command(label="New config", command=main.menu_new_config)
        self.menu_open.add_command(label="Open config", command=main.menu_open_config)
        self.menu_open.add_separator()
        self.menu_open.add_cascade(label="Recent config", menu=self.menu_recent_config)

        self.menu_help.add_command(label="Welcome", command=lambda: self.menu_welcome(main))
        self.menu_help.add_command(label="Tutorial", command=lambda: self.menu_tutorial(main))
        self.menu_help.add_command(label="About", command=lambda: self.menu_about(main))

        self.menu_report.add_cascade(label="Busload report", menu=self.menu_recent_report)
        self.menu_report.add_cascade(label="Side_by_side report", menu=self.menu_recent_side)

        self.menu_recent_config.add_command(label="Clear list", command=lambda: self._clear_recent_config(main))
        self.menu_recent_config.add_separator()

        self.menu_recent_report.add_command(label="Clear list", command=lambda: self._clear_recent_report(main))
        self.menu_recent_report.add_separator()

        self.menu_recent_side.add_command(label="Clear list", command=lambda: self._clear_recent_side(main))
        self.menu_recent_side.add_separator()

        main.config(menu=self)

    def menu_welcome(self, main):
        main.open_welcome_window()

    def menu_tutorial(self, main):
        main.open_tutorial_window()

    def menu_about(self, main):
        main.open_about_window()

    def _clear_recent_config(self, main):
        self.menu_recent_config.delete(2, self.menu_recent_config.index(tk.END))
        main.init_config['recent_config'] = []

    def _clear_recent_report(self, main):
        self.menu_recent_report.delete(2, self.menu_recent_report.index(tk.END))
        main.init_config['recent_report'] = []

    def _clear_recent_side(self, main):
        self.menu_recent_side.delete(2, self.menu_recent_side.index(tk.END))
        main.init_config['recent_side'] = []

    def menu_enable(self, item):
        self.entryconfig(item, state=tk.NORMAL)

    def recent_menu_update_config(self, config, main):
        for menu_item in config:
            self.menu_recent_config.add_command(label=menu_item, command=lambda sv=menu_item: main.open_config(sv))

    def recent_menu_update_report(self, config, main):
        for menu_item in config:
            self.menu_recent_report.add_command(label=menu_item, command=lambda sv=menu_item: main.open_html(sv))

    def recent_menu_update_side(self, config, main):
        for menu_item in config:
            self.menu_recent_side.add_command(label=menu_item, command=lambda sv=menu_item: main.open_html(sv))

    def remove_config(self):
        self.menu_recent_config.delete(2)

    def remove_report(self):
        self.menu_recent_report.delete(2)

    def remove_side(self):
        self.menu_recent_report.delete(2)


class StatusBar(tk.Frame):
    def __init__(self, main):
        tk.Frame.__init__(self, main, bd=1, relief=tk.SUNKEN)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        internal_frame = tk.Frame(self)
        internal_frame.grid(column=0, row=0, sticky='wens')
        internal_frame.columnconfigure(0, weight=1)
        internal_frame.rowconfigure(0, weight=0)
        self.responsible = tk.StringVar()
        self.msg = tk.StringVar()
        self._timeout = True
        self._list = []
        self._timeoutDefault = 3000
        self._timeoutValue = 3000
        self.list_mode = 0  # 0 = cyclic, 1 = pop
        self._list_index = 0
        self.msg.set('Busload Calc 2.1')
        self._jumpNext = False
        self._main = main
        self.msg_color = tk.StringVar()
        self.msg_color.set('black')
        tk.Label(internal_frame, text='Responsible').grid(row=0, column=0, padx=(10, 5), sticky='e')
        tk.Entry(internal_frame, width=25, textvariable=self.responsible).grid(row=0, column=1, padx=(0, 10),
                                                                               sticky='e')
        tk.Label(internal_frame, text='Hint:').grid(row=0, column=2, padx=5, sticky='e')
        tk.Label(internal_frame, textvariable=self.msg, fg=self.msg_color.get()).grid(row=0, column=3, columnspan=2, sticky='w')
        self.responsible.trace('w', lambda name, index, mode, sv=self.responsible: self.on_modify_entry(sv, main))
        self._call_timer()

    def on_modify_entry(self, sv, main, *args):
        main.init_config['responsible'] = self.responsible.get()

    def set_status_msg(self, text, time=0):
        self.msg.set(text)
        winsound.Beep(800, 50)

    def set_list(self, status_list):
        self._list = status_list
        self._list_index = 0

    def set_timeout(self, time):
        self._timeoutValue = time

    def set_timeout_on(self):
        self._timeout = True

    def set_timeout_off(self):
        self._timeout = False

    def set_time_default(self):
        self._timeoutValue = self._timeoutDefault

    def _call_timer(self):
        if self._timeout:
            if self._list:
                self._call_show_list()
            elif self.msg.get():
                self.msg.set('')

        self._main.after(self._timeoutValue, self._call_timer)

    def _call_show_list(self):
        self.msg_color.set('black')
        if self.list_mode == 0:
            i = len(self._list)
            if self._list_index >= i:
                self._list_index = 0
            self.msg.set(self._list[self._list_index])
            self._list_index += 1
        else:
            if self._list:
                self.msg.set(self._list.pop(0))
