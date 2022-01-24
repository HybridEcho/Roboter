#Import packages
import sys
from os import path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic

MW_Ui, MW_Base = uic.loadUiType('gui_view.ui')

class MainWindow(MW_Base, MW_Ui):
    events = {}

    def __init__(self):
        """MainWindow constructor. """
        super().__init__()
        self.setupUi(self)


        ##################
        # Connect Events #
        ##################

        self.control_play.clicked.connect(self.save_status)

        self.show()

    ##################
    # Methods #
    ##################
    def save_status(self):
        print("Hallo Hallo.")
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())




