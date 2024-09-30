import asyncio
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from core.system.settings import SystemSettings
from core.system.filesmanager import FilesManager
from ..session.webpage import SessionWebPage
from .gui.uis import *

class Window (QMainWindow):

    def __init__ (self):

        super().__init__()
        self.directory  = SystemSettings.files_manager_settings['ui_directory']
        self.widget     = QtWidgets.QStackedWidget()

        self.setWindowIcon(QtGui.QIcon(self.directory + 'img/logo.png'))
        self.setWindowTitle(SystemSettings.system_settings['name'])
        self.setFixedWidth(500)
        self.setFixedHeight(700)
        
        self.goToLayout('landing', True)
        self.setCentralWidget(self.widget)
        self.show()
        
    def goToLayout (self, name, init = False):

        layouts = {
            'landing': LandingUi,
            'index': IndexUi,
            'settings': SettingsUi,
            'session': SessionUi
        }

        layout = layouts.get(name)(self)
        self.widget.addWidget(layout)

        if init == False:
            self.widget.removeWidget(self.widget.currentWidget())
    
    def session_run (self):

        self.session_thread = threading.Thread(target=self.session_init)
        self.session_thread.start()

    def session_init (self):
        
        asyncio.run(self.browser_new())
    
    async def browser_new (self):

        browser = SessionWebPage()
        await browser.window_open()

        if SystemSettings.session_settings['mode_demo'] == False:
            await browser.login()

        await browser.launch()