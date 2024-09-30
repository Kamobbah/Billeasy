import sys
from PyQt5.QtWidgets import QApplication

from core.packages.app.window import Window

if __name__ == '__main__':

    app = QApplication(sys.argv)
    Window()

    try:
        sys.exit(app.exec())
    except:
        print('Application closed')