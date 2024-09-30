import asyncio
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from core.system.settings import SystemSettings
from core.system.filesmanager import FilesManager

class LandingUi (QDialog):

    def __init__ (self, widget):

        super(LandingUi, self).__init__()
        self.ui = widget
        loadUi(self.ui.directory + 'designer/landing.ui', self)
        self.autofill()

        self.loginBtn.clicked.connect( self.goToIndex )
        self.passwordIpt.setEchoMode( QtWidgets.QLineEdit.Password )

    def goToIndex (self):

        login = self.login()
        if login:
            self.ui.goToLayout('index')

    def autofill_state (self):

        state = FilesManager.autofill_get_state()

        if state:
            FilesManager.autofill_get_login()

        return state

    def autofill (self):

        state = self.autofill_state()

        if state:
            self.usernameIpt.setText(SystemSettings.user_settings['username'])
            self.passwordIpt.setText(SystemSettings.user_settings['password'])
            self.rememberChk.setChecked(True)

    def login (self):
        
        username = self.usernameIpt.text().replace(' ', '')
        password = self.passwordIpt.text().replace(' ', '')
        save = self.rememberChk.isChecked()

        if len(username) == 0 \
            or len(password) == 0:
            return self.errorLbl.setText('Veuillez remplir tous les champs.')
        
        else:
            SystemSettings.user_settings['username'] = username
            SystemSettings.user_settings['password'] = password

            FilesManager.autofill_save_state(save)
            FilesManager.autofill_save_login()

            return True