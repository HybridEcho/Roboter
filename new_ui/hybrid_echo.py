#Import packages
import sys
from os import path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from roboter_operation import RoboterOperation
from pxi_operation import PXIOperation

MW_Ui, MW_Base = uic.loadUiType('gui_view.ui')


class MainWindow(MW_Base, MW_Ui):

    def __init__(self):
        """MainWindow constructor. """
        super().__init__()
        self.setupUi(self)

        self.roboter_operation = RoboterOperation()
        self.pxi_operation = PXIOperation()

        ##################
        # Connect Events #
        ##################

        self.control_play.clicked.connect(self.roboter_operation.save_status)
        self.control_stop.clicked.connect(self.pxi_operation.status)

        ##################
        ##################

        self.show()
    



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())




