from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from core.system.settings import SystemSettings

class SessionUi (QDialog):

    def __init__ (self, widget):

        super(SessionUi, self).__init__()
        self.ui = widget
        loadUi(self.ui.directory + 'designer/session.ui', self)
        
        self.sessIdLbl.setText( SystemSettings.session_settings['session_id'] )
        self.stopBtn.clicked.connect( self.session_stop )

    def session_stop (self):

        SystemSettings.session_settings['statut'] = False
        self.ui.goToLayout('index')

    # TO DO
    def session_checking (self):

        while SystemSettings.session_settings['statut']:
            print('waiting')
        self.session_stop()