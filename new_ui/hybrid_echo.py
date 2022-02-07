#Import packages
import sys
import os
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from roboter_operation import RoboterOperation
#from pxi_operation import PXIOperation


os.chdir("C:/Users/Moritz/Documents/Code/Roboter/new_ui") #für Windows notwendig
MW_Ui, MW_Base = uic.loadUiType("gui_view.ui")


class MainWindow(MW_Base, MW_Ui):

    def __init__(self):
        """MainWindow constructor. """
        super().__init__()
        self.setupUi(self)

        self.roboter_operation = RoboterOperation()
        #self.pxi_operation = PXIOperation()

        ##################
        # Connect Events #
        ##################

        #self.control_play.clicked.connect(self.roboter_operation.save_status)
        self.load_position.clicked.connect(self.roboter_operation.get_position_blue)
        #self.control_stop.clicked.connect(self.pxi_operation.status)

        self.setup_servo_blue_on.clicked.connect(self.roboter_operation.servo_blue_on)
        self.setup_servo_blue_off.clicked.connect(self.roboter_operation.servo_blue_off)
        
        self.setup_servo_red_on.clicked.connect(self.roboter_operation.servo_red_on)
        self.setup_servo_red_off.clicked.connect(self.roboter_operation.servo_red_off)

        self.setup_load_blue.clicked.connect(self.populate_coordinates_blue)
        self.setup_load_red.clicked.connect(self.populate_coordinates_red)

        self.setup_goto_blue.clicked.connect(self.read_coordinates_blue)
        self.setup_goto_red.clicked.connect(self.read_coordinates_red)



        ##################
        ##################

        self.show()
    

    def populate_coordinates_blue(self, coordinates_blue):
        self.setup_blue_x.setValue(coordinates_blue[0])
        self.setup_blue_y.setValue(coordinates_blue[1])
        self.setup_blue_z.setValue(coordinates_blue[2])
        self.setup_blue_r.setValue(coordinates_blue[3])
    
    def populate_coordinates_red(self, coordinates_red):
        self.setup_red_x.setValue(coordinates_red[0])
        self.setup_red_y.setValue(coordinates_red[1])
        self.setup_red_z.setValue(coordinates_red[2])
        self.setup_red_r.setValue(coordinates_red[3])

    
    def read_coordinates_blue(self):
        x = self.setup_blue_x.value()
        y = self.setup_blue_y.value()
        z = self.setup_blue_z.value()
        r = self.setup_blue_r.value()

        coordinates = np.array([x, y, z, r])
    
    def read_coordinates_red(self):
        x = self.setup_red_x.value()
        y = self.setup_red_y.value()
        z = self.setup_red_z.value()
        r = self.setup_red_r.value()

        coordinates = np.array([x, y, z, r])



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())