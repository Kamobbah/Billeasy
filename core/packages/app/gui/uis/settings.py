from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import *

from core.system.filesmanager import FilesManager

class SettingsUi (QDialog):

    def __init__ (self, widget):

        super(SettingsUi, self).__init__()
        self.ui = widget
        loadUi(self.ui.directory + 'designer/settings.ui', self)
        
        self.backBtn.clicked.connect( self.back )
        self.saveBtn.clicked.connect( self.save )
        self.loadBtn.clicked.connect( self.load )
        self.defaultBtn.clicked.connect( self.default )
        
        self.timerStateEdit.clicked.connect( self.timer_state )
        self.quickStartEdit.clicked.connect( self.quick_start )

        self.set_settings()

    def back (self):

        if self.set_datas():
            self.ui.goToLayout('index')

    def save (self):
        
        pass

    def load (self):
        
        pass

    def default (self):
        
        pass

    def set_datas (self):
        
        timer = False
        mins = False
        max = False

        if self.timerStateEdit.isChecked():
            full = self.timerEdit.text().split(' ')
            date = full[0].split('/')
            time = full[1].split(':')

            timer = {
                'day': [int(date[0]), int(date[1]), int(date[2])],
                'time': [int(time[0]), int(time[1])]
            }

        if self.betMinsEdit.text() != '':
            mins = self.betMinsEdit.text().split(', ')

            for x in range(len(mins)):
                mins[x] = float(mins[x])
        
        if self.betMaxEdit.text() != '':
            max = float(self.betMaxEdit.text())

        settings = {
            'session': {
                'timer': timer
            },
            'frank': {
                'brain': self.brainEdit.currentText().lower(),
                'self_confidence': int(self.selfConfEdit.text()),
                'quick_start': self.quickStartEdit.isChecked()
            },
            'bets': {
                'set': float(self.betSetEdit.text()),
                'stop': float(self.betStopEdit.text()),
                'attempts_max': int(self.betAttemptsMaxEdit.text()),
                'attempts_min': int(self.betAttemptsMinEdit.text()),
                'mins': mins,
                'max': max,
                'condition': float(self.betConditionEdit.text()),
                'safety': float(self.betSafetyEdit.text())
            }
        }

        FilesManager.autofill_update_settings(settings)

        return True

    def set_settings (self):

        settings = FilesManager.autofill_get_settings()

        if settings['session']['timer']:
            date = settings['session']['timer']['day']
            time = settings['session']['timer']['time']
            year = date[2]
            month = date[1]
            day = date[0]
            hours = time[0]
            minutes = time[1]
            timer = QDateTime(year, month, day, hours, minutes)

            self.timerEdit.setDateTime(timer)
            self.timerStateEdit.setChecked(True)
            self.timer_state()
        
        else:
            currentTime = QDateTime.currentDateTime()
            self.timerEdit.setDateTime(currentTime)
            self.timerStateEdit.setChecked(False)
            self.timer_state()

        self.brainEdit.setCurrentText ( settings['frank']['brain'].capitalize() )
        self.selfConfEdit.setText( str(settings['frank']['self_confidence']) )
        self.betSetEdit.setText( str(settings['bets']['set']) )
        self.betStopEdit.setText( str(settings['bets']['stop']) )
        self.betAttemptsMaxEdit.setText( str(settings['bets']['attempts_max']) )
        self.betAttemptsMinEdit.setText( str(settings['bets']['attempts_min']) )
        self.betConditionEdit.setText( str(settings['bets']['condition']) )
        self.betSafetyEdit.setText( str(settings['bets']['safety']) )

        if settings['bets']['mins']:
            self.betMinsEdit.setText( ', '.join(str(e) for e in settings['bets']['mins']) )
        else:
            self.betMinsEdit.setText('')

        if settings['bets']['max']:
            self.betMaxEdit.setText( str(settings['bets']['max']) )
        else:
            self.betMaxEdit.setText('') 

        if settings['frank']['quick_start']:
            self.quickStartEdit.setChecked(True)
            self.quick_start()
        else:
            self.quickStartEdit.setChecked(False)
            self.quick_start()

    def verification (self, settings):

        print(settings)
        certified = []

        if (type(int(settings['self_confidence'])) != 'int'):
            certified.append(False)
            print('Self Confidence must be a number')
        elif int(settings['self_confidence']) < 0:
            certified.append(True)
        else:
            certified.append(False)
            print('Self Confidence must be superior or equal to 0')

    def timer_state (self):
        
        timer_state = self.timerStateEdit.isChecked()

        if timer_state:
            self.timerStateEdit.setText('Activated')
            return True
        
        else:
            self.timerStateEdit.setText('Desactivated')
            return False

    def quick_start (self):
        
        quick_start = self.quickStartEdit.isChecked()

        if quick_start:
            self.quickStartEdit.setText('Activated')
            return True
        
        else:
            self.quickStartEdit.setText('Desactivated')
            return False
