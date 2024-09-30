from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from core.system.system import System
from core.system.settings import SystemSettings
from core.system.filesmanager import FilesManager

class IndexUi (QDialog):

    def __init__ (self, widget):

        super(IndexUi, self).__init__()
        self.ui = widget
        loadUi(self.ui.directory + 'designer/index.ui', self)
        
        self.wlcUsernameLbl.setText( SystemSettings.user_settings['username'] )
        self.logoutBtn.clicked.connect( lambda: self.ui.goToLayout('landing') )
        self.settingsBtn.clicked.connect( lambda: self.ui.goToLayout('settings') )
        self.demoBtn.clicked.connect( lambda: self.start_session(True) )
        self.realBtn.clicked.connect( lambda: self.start_session(False) )

    def start_session (self, mode_demo):

        System.session_set()
        FilesManager.autofill_set_settings()
        SystemSettings.user_settings['wallet'] = float(self.walletEdit.text())
        SystemSettings.session_settings['mode_demo'] = mode_demo
        SystemSettings.session_settings['statut'] = True
        self.ui.session_run()
        self.ui.goToLayout('session')