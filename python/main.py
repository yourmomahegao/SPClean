import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog
from interface import Ui_MainWindow

import ctypes
import os
import shutil
from pathlib import Path


# Check is app is on admin mode
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def showAdminDialog():
    dlg = QDialog()
    dlg.setWindowTitle("SPClean - Уведомление")
    dlg.setWindowIcon(QtGui.QIcon(':/icons/rec/icon-transparent.png'))
    dlg.setObjectName("Dialog")
    dlg.resize(500, 61)
    dlg.setStyleSheet("QWidget {\n"
                      "    background-color: rgb(30, 30, 30);\n"
                      "    color: rgb(230, 230, 230);\n"
                      "    border-radius: 5px;\n"
                      "    font: 16pt \"Ermilov\";\n"
                      "}\n"
                      "")

    dlg_verticalLayout = QtWidgets.QVBoxLayout(dlg)
    dlg_verticalLayout.setObjectName("verticalLayout")
    dlg_label_2 = QtWidgets.QLabel(dlg)

    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(dlg_label_2.sizePolicy().hasHeightForWidth())

    dlg_label_2.setSizePolicy(sizePolicy)
    dlg_label_2.setStyleSheet("QLabel {\n"
                              "    font: 12pt \"Ermilov\";\n"
                              "}")
    dlg_label_2.setAlignment(QtCore.Qt.AlignCenter)
    dlg_label_2.setWordWrap(True)
    dlg_label_2.setObjectName("label_2")
    dlg_verticalLayout.addWidget(dlg_label_2)

    dlg_label_2.setText("Приложение может работать неправильно, запустите его от имени администратора")

    dlg.exec()


class ProgramUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(ProgramUI, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/rec/icon-transparent.png'))
        self.setWindowTitle("SPClean")
        self.setMinimumSize(900, 600)

        # Admin rights check
        self.checkAdminRights()

        # Connecting button
        self.connectButtons()

        # Checkboxes list
        self.profiles = [
            self.ui.temp_clear,
            self.ui.downloads_clear,
            self.ui.desktop_clear,
            self.ui.autorun_clear,
            self.ui.processes_clear
        ]

    # Checking admin rights
    @staticmethod
    def checkAdminRights():
        if not isAdmin():
            showAdminDialog()

    # Connecting buttons
    def connectButtons(self):
        self.ui.disc_space_button.clicked.connect(self.discSpaceProfileLoad)
        self.ui.processes_button.clicked.connect(self.processesProfileLoad)
        self.ui.autorun_button.clicked.connect(self.autorunProfileLoad)
        self.ui.run_clear.clicked.connect(self.runClear)

    # Disc space profile
    def discSpaceProfileLoad(self):
        profile_buttons = [self.ui.temp_clear, self.ui.downloads_clear, self.ui.desktop_clear]

        # Setting up buttons for chosen profile
        for button in self.profiles:
            try:
                profile_buttons.index(button)
            except ValueError:
                button.setChecked(False)
            else:
                button.setChecked(True)

    # Processes profile
    def processesProfileLoad(self):
        profile_buttons = [self.ui.processes_clear]

        # Setting up buttons for chosen profile
        for button in self.profiles:
            try:
                profile_buttons.index(button)
            except ValueError:
                button.setChecked(False)
            else:
                button.setChecked(True)

    # Autorun profile
    def autorunProfileLoad(self):
        profile_buttons = [self.ui.autorun_clear]

        # Setting up buttons for chosen profile
        for button in self.profiles:
            try:
                profile_buttons.index(button)
            except ValueError:
                button.setChecked(False)
            else:
                button.setChecked(True)

    # Clear all files in directory
    @staticmethod
    def clearDirectory(dirpath: str):
        # Get all files in directory
        dirlist = os.listdir(dirpath)

        # Clearing all files in dir
        for _item in dirlist:
            try:
                # Removing tree if file is dir
                if os.path.isdir(f'{dirpath}\\{_item}'):
                    shutil.rmtree(f'{dirpath}\\{_item}')
                else:
                    os.remove(f'{dirpath}\\{_item}')
            except Exception as ex:
                print(ex)

            try:
                # If file is EMPTY dir, removing
                if os.path.isdir(f'{dirpath}\\{_item}'):
                    os.rmdir(f'{dirpath}\\{_item}')
            except Exception as ex:
                print(ex)

    # Clear temp files
    def clearTemp(self):
        # Get temp file directory
        temp_path = os.getenv("TEMP")
        self.clearDirectory(temp_path)

    # Clear downloads folder
    def clearDownloads(self):
        # Get downloads path
        downloads_path = str(Path.home() / "Downloads")
        self.clearDirectory(downloads_path)

    # Clear user desktop
    @staticmethod
    def clearDesktop():
        # Working with paths
        desktop_path = os.path.normpath(os.path.expanduser("~/Desktop"))
        new_dir_path = f'{desktop_path}\\Элементы рабочего стола'
        do_not_touch_ext = 'lnk', 'exe'
        do_not_touch_dirs = True

        # Get list of all files in dir
        dirlist = os.listdir(desktop_path)

        # Checking is file in blacklist
        def isDoNotTouch(extension: str):
            for ext in do_not_touch_ext:
                if _extension == ext:
                    return True

            return False

        try:
            os.mkdir(new_dir_path)
        except Exception as ex:
            print(ex)

        for _item in dirlist:
            if not os.path.isdir(f'{desktop_path}\\{_item}') or do_not_touch_dirs is False:
                _extension = _item.split('.')[-1]

                if not isDoNotTouch(_extension):
                    try:
                        shutil.move(f'{desktop_path}\\{_item}', new_dir_path)
                    except Exception as ex:
                        print(ex)

    # Clear autorun list
    def clearAutorun(self):
        self.clearDirectory(f'{os.getenv("APPDATA")}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        self.clearDirectory(f'{os.getenv("PROGRAMDATA")}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Clear whitelist processes
    @staticmethod
    def clearProcesses():
        import psutil

        # Processes that we are able to terminate
        whitelist = ['chrome.exe', 'yandex.exe', 'Discord.exe', 'DiscordUpdater.exe', 'steam.exe', 'photoshop.exe', 'cmd.exe']

        # Check is file in whitelist or not
        def isInWhitelist(name: str):
            for whitelist_name in whitelist:
                if whitelist_name == name:
                    return True

            return False

        # Getting all processes that are running at this time
        for proc in psutil.process_iter(attrs=['username', 'cpu_percent']):
            try:
                # Getting process name
                processName = proc.name()

                # Trying to get who rules the process
                try:
                    processUser = proc.username().split('\\')[-1]
                except IndexError:
                    processUser = proc.username()

                # Getting how mush of memory is used by the process
                processMemory = round(proc.memory_info().vms / (1024 * 1024))

                # If process is
                # - In whitelist;
                # - Ruled by current user
                # - Uses more than 30 megabytes of memory, terminating it
                if isInWhitelist(processName) \
                        and processUser == os.environ.get("USERNAME") \
                        and processMemory > 30:
                    print(processName, ' ::: ', processUser, ' ::: ', processMemory)
                    proc.kill()

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    # Clear run
    def runClear(self):
        # Connecting checkboxes to their functions
        if self.ui.temp_clear.isChecked():
            self.clearTemp()

        if self.ui.downloads_clear.isChecked():
            self.clearDownloads()

        if self.ui.desktop_clear.isChecked():
            self.clearDesktop()

        if self.ui.autorun_clear.isChecked():
            self.clearAutorun()

        if self.ui.processes_clear.isChecked():
            self.clearProcesses()


app = QtWidgets.QApplication([])
a = ProgramUI()
a.show()

sys.exit(app.exec())
