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


#os.chdir("C:/Users/Moritz/Documents/Code/Roboter/new_ui") #für Windows notwendig
os.chdir("/Users/julian/Documents/HybridEcho/Roboter/new_ui")
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
        #self.control_stop.clicked.connect(self.pxi_operation.status)



        ## setup ##

        # self.setup_servo_blue_on.clicked.connect(self.roboter_operation.servo_blue_on)
        # self.setup_servo_blue_off.clicked.connect(self.roboter_operation.servo_blue_off)
        
        # self.setup_servo_red_on.clicked.connect(self.roboter_operation.servo_red_on)
        # self.setup_servo_red_off.clicked.connect(self.roboter_operation.servo_red_off)

        self.setup_load_blue.clicked.connect(self.populate_coordinates_blue)
        self.setup_load_red.clicked.connect(self.populate_coordinates_red)

        self.setup_goto_blue.clicked.connect(self.read_coordinates_blue)
        self.setup_goto_red.clicked.connect(self.read_coordinates_red)

        
        ## rotation ##

        self.rotation_calculate.clicked.connect(self.rotation_calculation)


        ## checklist ##
        self.checklist_save_csv.clicked.connect(self.save_csv)


        ##################
        ##################

        self.show()


    

    def test_method(self, nr):        
        nr = RoboterOperation.callcalc()
        RoboterOperation.printer(self, nr)
        

    def populate_coordinates_blue(self):
        coordinates_blue = np.array([1.11, 2.22, 3.33, 4.44]) #ersetzen
        self.setup_blue_x.setValue(coordinates_blue[0])
        self.setup_blue_y.setValue(coordinates_blue[1])
        self.setup_blue_z.setValue(coordinates_blue[2])
        self.setup_blue_r.setValue(coordinates_blue[3])
    
    def populate_coordinates_red(self, coordinates_red):
        coordinates_red = np.array([1.11, 2.22, 3.33, 4.44]) #ersetzen
        self.setup_red_x.setValue(coordinates_red[0])
        self.setup_red_y.setValue(coordinates_red[1])
        self.setup_red_z.setValue(coordinates_red[2])
        self.setup_red_r.setValue(coordinates_red[3])

    
    
    def read_coordinates_blue(self):
        x = self.setup_blue_x.value()
        y = self.setup_blue_y.value()
        z = self.setup_blue_z.value()
        r = self.setup_blue_r.value()

        coordinates_blue = np.array([x, y, z, r])
        return coordinates_blue

    
    def read_coordinates_red(self):
        x = self.setup_red_x.value()
        y = self.setup_red_y.value()
        z = self.setup_red_z.value()
        r = self.setup_red_r.value()

        coordinates_red = np.array([x, y, z, r])
        return coordinates_red

    def rotation_calculation(self):
        angle_step_size = self.rotation_angle_step_size.value()
        total_rotation = self.rotation_total_rotation.value()
        #rotation_distance = self.rotation_distance.value()

        coordinates_blue = self.read_coordinates_blue()
        coordinates_red = self.read_coordinates_red()

        global calibration_rotation_dataframe
        calibration_rotation_dataframe = RoboterOperation.calibration_calculation(angle_step_size, total_rotation, coordinates_blue, coordinates_red)

    
    def save_csv(self):
        filename = "/Users/julian/Documents/HybridEcho/Roboter/new_ui/test.csv"
        RoboterOperation.save_to_csv(self, calibration_rotation_dataframe, filename)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
