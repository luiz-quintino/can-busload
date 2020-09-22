import tkinter as tk
import frame_config as ConfigFrame, frame_result as ResultFrame
import drawble as r
import config as Config
import const as Const
import util
from file_name import FileName


class Child(tk.Toplevel):
    def __init__(self, main, conf=Config, title=''):
        tk.Toplevel.__init__(self, main)

        self.geometry('400x490' + main.get_child_window_position())
        #self.resizable(0, 0)
        self.minsize(400, 490)
        #self.maxsize(460, 520)
        self.transient(main)
        self.iconbitmap(r.ICO_CHILD)
        self.wm_protocol("WM_DELETE_WINDOW", lambda: self.quit(self.winfo_id()))

        # Initialize
        self.main = main
        self.bind('<Configure>', main.state_child)  # Handle windows movement
        self._frame = None  # Initialize frames
        self.menu = CreateMenu(self)  # Creates menu bar
        self.cnf = conf.cnf  # Manage configuration
        self.calc = conf.result  # Manage calc
        self.log = conf.log
        self.dbc = conf.dbc
        self.nodes = []
        self.frm_conf = None  # Parameter for listFrame
        self.saved = True if title else False
        self.file_config = conf.config_name
        self.file_dbc = conf.dbc_name
        self.last_html = ''
        self.last_csv = ''
        self.new = False if title else True

        if title:
            self.cnf = util.reading_json(self.file_config.get_full_name(), self)

        if not title:
            title = self.get_title()
            conf.config_name = self.file_config = FileName(title + '.cnf')

        if not self.cnf:
            self._load_default_config()
            if main.init_config.get('responsible'):
                self.cnf['responsible'] = main.init_config.get('responsible')

        self.title(title)
        self.switch_frame(ConfigFrame.StartPage)

    def quit(self, my_id):
        if not self.saved:
            self.ask_to_save()
        self.main.quit_child(my_id)

    def duplicate_config(self):
        self.main.open_duplicated_config(self.cnf)

    def main_mesage_box(self, message, box_type=Const.MSG_INFO):
        self.main.main_mesage_box(message, box_type)

    def status_bar_text(self, text, time=0):
        self.main.status_bar.set_status_msg(text, time)

    def status_bar_list(self, status_list):
        self.main.status_bar.set_list(status_list)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

    def run_calc(self):
        if not self.saved:
            if not self.ask_to_save():
                return

        if self.check_dbc():
            conf = Config
            conf.cnf = self.cnf
            conf.dbc = self.dbc
            config = self.main.run_calc(conf)
            if config:
                self.log = config.log
                self.calc = config.result
                if config.cnf.get('html').lower() == 'true':
                    name = "output/" + self.file_dbc.file_name + "_busload_" + util.get_date(0) + ".html"
                    if util.save_output_html(name, config):
                        self.last_html = name
                        self.main.add_recent_report(name)
                if config.cnf.get('csv').lower() == 'true':
                    name = "output/" + self.file_dbc.file_name + "_busload_" + util.get_date(0) + ".csv"
                    if util.save_output_csv(name, config):
                        self.last_csv = name
                self.switch_frame(ResultFrame.ResultFrame)
        else:
            self.main.main_mesage_box('Not possible to calc. Missing dbc message.')

    def open_last_html(self):
        if self.last_html:
            self.main.open_html(self.last_html)

    def open_last_csv(self):
        if self.last_csv:
            self.main.open_csv(self.last_csv)

    def open_dbc(self):
        dbc = self.main.menu_open_dbc()
        self.file_dbc = dbc
        return dbc

    def ask_to_save(self):
        if not self.main.main_mesage_box('Configuration "{}" not saved.\nSave it now?'.format(self.file_config.file_name), Const.MSG_YES_NO):
            return False

        self.status_bar_text("Saving configuration to execute Busload Calc...")
        self._frame.update_config()
        self.save()
        return True

    def check_dbc(self):
        if self.cnf.get('dbc'):
            self.file_dbc = FileName(self.cnf.get('dbc'))
            self.dbc = util.get_db_file(self.file_dbc.get_full_name(), self)
            if self.dbc:
                return True
        return False

    def save(self):
        if self.new:
            self.save_as()
            return

        self._frame.update_config()
        txt_config = self._frame.txt[Const.TXT_CONFIG_NAME].get()
        title = self.file_config

        if txt_config != title.file_name:
            if self.main.main_mesage_box('The config name was change from: "{0}" to "{1}"\n\n'
                                         'Click OK to save as "{1}"\n'
                                         'Click CANCEL to maintain "{0}"'.format(title.file_name,
                                                                               txt_config), Const.MSG_OK_CANCEL):
                self.save_as()
                return

        if util.writing_json(self.cnf, title.get_full_name(), self):
            self.title(title.file_name)
            self.saved = True

    def save_as(self):
        self._frame.update_config()
        config_file = FileName(self._frame.txt[Const.TXT_CONFIG_NAME].get())

        title = self.main.menu_save_as(config_file)
        if title.file_name:
            self.file_config = title
            self._frame.txt[Const.TXT_CONFIG_NAME].set(title.file_name)
            if util.writing_json(self.cnf, title.get_full_name(), self):
                self.title(title.file_name)
                self.saved = True
                self.new = False
                self.main.add_recent_config(title.get_full_name())

    def on_modify_config(self):
        if self.saved:
            self.saved = False
            if self.title()[-1] != '*':
                self.title(self.title() + '*')

    def get_title(self):
        index = self.main.init_config.get('index_title') + 1
        if index > 999:
            index = 0
        self.main.init_config['index_title'] = index
        return "New_Config_{:03d}".format(index)

    def child_quit(self):
        if not self.saved:
            self.ask_to_save()
        self.main.quit_child(self.winfo_id())

    def _load_default_config(self):
        self.cnf = {
            'Busload Calc configuration': '2020',
            'version': '2.1',
            'dbc': '',
            'responsible': '',
            'description': '',
            'label': '',
            'bit_stuffing': 25,
            'baudrate': 500,
            'id_size': 'Auto',
            'screen': "true",
            'csv': "false",
            'html': "true",
            'modify_message': {},
            'add_message': {},
            'dbc_combine': {'dbc_list': [], 'ecus': [], 'messages': {}},
            'erase_ecu': [],
            'erase_message': [],
            'graph': 'clock'
        }


class CreateMenu(tk.Menu):
    def __init__(self, child):
        tk.Menu.__init__(self, child)

        self.file_menu = self
        self.file_menu.add_command(label="Save", command=lambda: self._menu_save(child))
        self.file_menu.add_command(label="Save as", command=lambda: self._menu_save_as(child))
        self.file_menu.add_command(label="Duplicate", command=lambda: self._menu_duplicate_config(child))
        self.file_menu.add_command(label="Run Calc", command=lambda: self._menu_run_calc(child))
        self.file_menu.add_command(label="Exit", command=lambda: self.menu_quit(child))
        self.menu_default()

        child.config(menu=self)

    def menu_quit(self, child):
        child.child_quit()

    def menu_disable(self, item):
        pass

    def menu_enable(self, item):
        self.entryconfig(item, state=tk.NORMAL)

    def menu_default(self):
        for i in range(1, 2):
            self.menu_disable(i)

    def _menu_duplicate_config(self, child):
        child.duplicate_config()

    def _menu_run_calc(self, child):
        child.run_calc()

    def _menu_save(self, child):
        child.save()

    def _menu_save_as(self, child):
        child.save_as()
