#Import packages
from inspect import Parameter
import sys
import os
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from roboter_operation import RoboterOperation
from parameter import network_parameters
#from pxi_operation import PXIOperation


os.chdir("C:/Users/Moritz/Documents/Code/Roboter/new_ui") #für Windows
#os.chdir("/Users/julian/Documents/HybridEcho/Roboter/new_ui") #für macOS
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


        ## setup ##

        self.setup_servo_blue_on.clicked.connect(self.servo_blue_on)
        self.setup_servo_blue_off.clicked.connect(self.servo_blue_off)
        
        self.setup_servo_red_on.clicked.connect(self.servo_red_on)
        self.setup_servo_red_off.clicked.connect(self.servo_red_off)

        self.setup_load_blue.clicked.connect(self.load_blue)
        self.setup_load_red.clicked.connect(self.load_red)

        self.setup_goto_blue.clicked.connect(self.goto_blue)
        self.setup_goto_red.clicked.connect(self.goto_red)

        self.setup_set_start_point.clicked.connect(self.set_start_point)
        
        ## rotation ##

        self.rotation_calculate.clicked.connect(self.rotation_calculation)


        ## checklist ##
        self.checklist_save_csv.clicked.connect(self.save_csv)
        self.checklist_start_measurement.clicked.connect(self.start_measurement)


        ##################
        ##################

        self.show()



    def servo_blue_on(self):
        RoboterOperation.roboter_message(self, network_parameters.tnblue, "C:R:SERVO_ON", "R:C:SERVO_ON")
    
    def servo_blue_off(self):
        RoboterOperation.roboter_message(self, network_parameters.tnblue, "C:R:SERVO_OFF", "R:C:SERVO_OFF")

    def servo_red_on(self):
        RoboterOperation.roboter_message(self, network_parameters.tnred, "C:R:SERVO_ON", "R:C:SERVO_ON")

    def servo_red_off(self):
        RoboterOperation.roboter_message(self, network_parameters.tnred, "C:R:SERVO_OFF", "R:C:SERVO_OFF")
        
    
    def set_start_point(self):
        global coordinates_blue, coordinates_red
        coordinates_blue = self.read_coordinates_blue()
        coordinates_red = self.read_coordinates_red()


    def populate_coordinates_blue(self, coordinates_blue):
        #coordinates_blue = np.array([1.11, 2.22, 3.33, 4.44]) #ersetzen
        self.setup_blue_x.setValue(coordinates_blue[0])
        self.setup_blue_y.setValue(coordinates_blue[1])
        self.setup_blue_z.setValue(coordinates_blue[2])
        self.setup_blue_r.setValue(coordinates_blue[3])
    
    def populate_coordinates_red(self, coordinates_red):
        #coordinates_red = np.array([1.11, 2.22, 3.33, 4.44]) #ersetzen
        self.setup_red_x.setValue(coordinates_red[0])
        self.setup_red_y.setValue(coordinates_red[1])
        self.setup_red_z.setValue(coordinates_red[2])
        self.setup_red_r.setValue(coordinates_red[3])

    
    def read_coordinates_blue(self):
        x = self.setup_blue_x.value()
        y = self.setup_blue_y.value()
        z = self.setup_blue_z.value()
        r = self.setup_blue_r.value()

        coordinates_blue = [x, y, z, r]
        return coordinates_blue

    
    def read_coordinates_red(self):
        x = self.setup_red_x.value()
        y = self.setup_red_y.value()
        z = self.setup_red_z.value()
        r = self.setup_red_r.value()

        coordinates_red = [x, y, z, r]
        return coordinates_red

    def load_blue(self):
        robo_message = RoboterOperation.roboter_message(self, network_parameters.tnblue, "C:R:CURRENT_POSITION", "R:C:CURRENT_POSITION")
        coordinates_blue = RoboterOperation.message_parser(self, robo_message)
        self.populate_coordinates_blue(coordinates_blue)

    def load_red(self):
        robo_message = RoboterOperation.roboter_message(self, network_parameters.tnred, "C:R:CURRENT_POSITION", "R:C:CURRENT_POSITION")
        coordinates_red = RoboterOperation.message_parser(self, robo_message)
        self.populate_coordinates_red(coordinates_red)


    def goto_blue(self):
        coordinates_blue = self.read_coordinates_blue()
        coordinates_message = RoboterOperation.message_assembler(self, coordinates_blue)
        robo_message = RoboterOperation.roboter_message_move(self, network_parameters.tnblue, "C:R:GOTO_POSITION", coordinates_message, "R:C:GOTO_POSITION")
        coordinates_blue = RoboterOperation.message_parser(self, robo_message)
        self.populate_coordinates_blue(coordinates_blue)

    
    def goto_red(self):
        coordinates_red = self.read_coordinates_red()
        coordinates_message = RoboterOperation.message_assembler(self, coordinates_red)
        robo_message = RoboterOperation.roboter_message_move(self, network_parameters.tnred, "C:R:GOTO_POSITION", coordinates_message, "R:C:GOTO_POSITION")
        coordinates_red = RoboterOperation.message_parser(self, robo_message)
        self.populate_coordinates_red(coordinates_red)


    def rotation_calculation(self):
        angle_step_size = self.rotation_angle_step_size.value()
        total_rotation = self.rotation_total_rotation.value()
        #rotation_distance = self.rotation_distance.value()

        global calibration_rotation_dataframe
        calibration_rotation_dataframe = RoboterOperation.calibration_calculation(angle_step_size, total_rotation, coordinates_blue, coordinates_red)

    
    def save_csv(self):
        filename = "C:/Users/Moritz/Documents/Code/Roboter/new_ui/test.csv"
        RoboterOperation.save_to_csv(self, calibration_rotation_dataframe, filename)

    def start_measurement(self):
        calibration_rotation_blue = calibration_rotation_dataframe[["Blue_X","Blue_Y","Blue_Z", "Blue_R"]].to_numpy()
        calibration_rotation_red = calibration_rotation_dataframe[["Red_X","Red_Y","Red_Z", "Red_R"]].to_numpy()

        coordinates_message_red = RoboterOperation.message_assembler(self, calibration_rotation_red[0])
        robo_message_red = RoboterOperation.roboter_message_move(self, network_parameters.tnred, "C:R:GOTO_POSITION", coordinates_message_red, "R:C:GOTO_POSITION")
        coordinates_red = RoboterOperation.message_parser(self, robo_message_red)
        self.populate_coordinates_red(coordinates_red)

        for i in range(len(calibration_rotation_blue)):
            coordinates_message_blue = RoboterOperation.message_assembler(self, calibration_rotation_blue[i])
            robo_message_blue = RoboterOperation.roboter_message_move(self, network_parameters.tnblue, "C:R:GOTO_POSITION", coordinates_message_blue, "R:C:GOTO_POSITION")
            coordinates_blue = RoboterOperation.message_parser(self, robo_message_blue)
            self.populate_coordinates_blue(coordinates_blue)
            self.progressBar.setValue(((i+1)*100)/len(calibration_rotation_dataframe))
        
        print("finished measurement")





if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
