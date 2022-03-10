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
from roboter_operation import RoboterOperation as RobOp
from parameter import network_parameters
from parameter import udp_messages
from pxi_operation import PXIOperation as PXIOp
import time


os.chdir("C:/Users/Moritz/Documents/Code/Roboter/new_ui") #für Windows
#os.chdir("/Users/julian/Documents/HybridEcho/Roboter/new_ui") #für macOS
MW_Ui, MW_Base = uic.loadUiType("gui_view.ui")


class RoboterController(qtc.QObject):

    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(float)
    current_coordinates_blue = qtc.pyqtSignal(list)
    current_coordinates_red = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()


    @qtc.pyqtSlot(pd.DataFrame)
    def measurement_loop(self, measurement_dataframe):
        print("Welcome to measurement loop")

        measurement_array_blue = measurement_dataframe[["Blue_X","Blue_Y","Blue_Z", "Blue_R"]].to_numpy()
        measurement_array_red = measurement_dataframe[["Red_X","Red_Y","Red_Z", "Red_R"]].to_numpy()

        for i in range(len(measurement_dataframe)):

            coordinates_message_blue = RobOp.message_assembler(self, measurement_array_blue[i])
            coordinates_message_red = RobOp.message_assembler(self, measurement_array_red[i])
            robo_message_blue = RobOp.roboter_message_move(self, network_parameters.tnblue, "C:R:GOTO_POSITION", coordinates_message_blue, "R:C:GOTO_POSITION")
            robo_message_red = RobOp.roboter_message_move(self, network_parameters.tnred, "C:R:GOTO_POSITION", coordinates_message_red, "R:C:GOTO_POSITION")
            coordinates_blue = RobOp.message_parser(self, robo_message_blue)
            coordinates_red = RobOp.message_parser(self, robo_message_red)
            
            self.current_coordinates_blue.emit(coordinates_blue)
            self.current_coordinates_red.emit(coordinates_red)

            time.sleep(0.2)
            #PXIOp.UDP_connection_PXI(self,udp_messages.message_PXI_reached_position, udp_messages.response_PXI_reached_position)
            #PXIOp.UDP_connection_PXI(self,udp_messages.message_PXI_Log_coord +f"Coordinates Blue (X,Y,Z,R): {coordinates_message_blue}" + "\t" + f"Coordinates Red (X,Y,Z,R): {coordinates_message_red} \n" , udp_messages.response_PXI_Log_coord)
        
            print("finished measurement")

            self.progress.emit((i+1)/len(measurement_dataframe))

        self.finished.emit()


class MainWindow(MW_Base, MW_Ui):
    
    #########################
    # Definition of signals #
    #########################
    
    initialize_measurement_finished = qtc.pyqtSignal(pd.DataFrame)

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self.setupUi(self)

        ##################
        # Initialization #
        ##################

        ##initialization of GUI##
        self.preview_blue_turning.setVisible(False)
        self.preview_red_turning.setVisible(False)
        self.preview_no_turning.setVisible(True)

        self.status_progressbar.setValue(0)

        ##Initialization of variables##
        self.checklist_done = False
        self.lineedit_done = False
        self.which_robot = None
        self.which_mode = "Calibration"

        self.coordinates_blue = [0, 0, 0, 0]
        self.coordinates_red = [0, 0, 0, 0]

        self.angle_step_size = 0
        self.total_rotation = 0
        self.rotation_distance = 0

        self.calibration_rotation_dataframe = pd.DataFrame(columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])
        self.bscan_dataframe = pd.DataFrame(columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])
        self.linear_array_dataframe = pd.DataFrame(columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])
        self.two_d_array_dataframe = pd.DataFrame(columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])



        ########################
        # Connection of Events #
        ########################

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
        
        ##documentation##

        self.documentation_name_measurement.textChanged.connect(self.lineedit_checker)
        self.documentation_measurement_notes.textChanged.connect(self.lineedit_checker)


        ## mode selection##
        self.planning_tab.currentChanged.connect(self.mode_state)

        ## rotation ##

        self.rotation_calculate.clicked.connect(self.rotation_calculation)

        ## checklist ##
        self.checklist_save_csv.clicked.connect(self.save_csv)
        self.checklist_checkBox_1.stateChanged.connect(self.checklist_checker)
        self.checklist_checkBox_2.stateChanged.connect(self.checklist_checker)
        self.checklist_checkBox_3.stateChanged.connect(self.checklist_checker)
        self.checklist_checkBox_4.stateChanged.connect(self.checklist_checker)
        self.checklist_checkBox_5.stateChanged.connect(self.checklist_checker)

        self.checklist_start_measurement.clicked.connect(self.proceed_to_measurement)

        ##rotation##
        self.rotation_blue_robot.toggled.connect(self.preview_state)
        self.rotation_blue_robot.toggled.connect(self.robot_selection)
        self.rotation_red_robot.toggled.connect(self.preview_state)
        self.rotation_red_robot.toggled.connect(self.robot_selection)

        ##linear array##
        self.lin_pushButton_1.clicked.connect(self.adapt_graph)


        ##measurement##
        self.control_play.clicked.connect(self.initialize_measurement)

        #############
        # Threading #
        #############
        
        self.roboter_controller = RoboterController()
        self.thread = qtc.QThread()
        self.roboter_controller.moveToThread(self.thread)

        #Connect signals and slots
        self.roboter_controller.finished.connect(self.thread.quit)
        
        #Start the thread
        self.thread.start()

        self.control_play.clicked.connect(self.thread.start)

        self.roboter_controller.progress.connect(self.report_progress)

        self.roboter_controller.current_coordinates_blue.connect(self.populate_coordinates_blue)
        self.roboter_controller.current_coordinates_red.connect(self.populate_coordinates_red)

        self.initialize_measurement_finished.connect(self.roboter_controller.measurement_loop)

        
        ##################
        ##################

        self.show()

    #######################
    # Definition of Slots #
    #######################

    @qtc.pyqtSlot()
    def servo_blue_on(self):
        RobOp.roboter_message(self, network_parameters.tnblue, "C:R:SERVO_ON", "R:C:SERVO_ON")


    @qtc.pyqtSlot()
    def servo_blue_off(self):
        RobOp.roboter_message(self, network_parameters.tnblue, "C:R:SERVO_OFF", "R:C:SERVO_OFF")


    @qtc.pyqtSlot()
    def servo_red_on(self):
        RobOp.roboter_message(self, network_parameters.tnred, "C:R:SERVO_ON", "R:C:SERVO_ON")


    @qtc.pyqtSlot()
    def servo_red_off(self):
        RobOp.roboter_message(self, network_parameters.tnred, "C:R:SERVO_OFF", "R:C:SERVO_OFF")
        

    @qtc.pyqtSlot()
    def checklist_checker(self):
        if self.checklist_checkBox_1.isChecked() == True and self.checklist_checkBox_2.isChecked() == True and self.checklist_checkBox_3.isChecked() == True and self.checklist_checkBox_4.isChecked() == True and self.checklist_checkBox_5.isChecked() == True:
            self.checklist_done = True
        else:
            self.checklist_done = False
        self.proceed_to_measurement_state()


    @qtc.pyqtSlot()
    def lineedit_checker(self):
        if self.documentation_name_measurement.text() and self.documentation_measurement_notes.text():
            self.lineedit_done = True
        else:
            self.lineedit_done = False
        self.proceed_to_measurement_state()
  
    
    @qtc.pyqtSlot()
    def proceed_to_measurement(self):
        self.tab_widget.setCurrentIndex(1)


    @qtc.pyqtSlot()
    def preview_state(self):
        if self.rotation_blue_robot.isChecked() == True:
            self.preview_blue_turning.setVisible(True)
            self.preview_red_turning.setVisible(False)
            self.preview_no_turning.setVisible(False)
        elif self.rotation_red_robot.isChecked() == True:
            self.preview_blue_turning.setVisible(False)
            self.preview_red_turning.setVisible(True)
            self.preview_no_turning.setVisible(False)
        else:
            self.preview_blue_turning.setVisible(False)
            self.preview_red_turning.setVisible(False)
            self.preview_no_turning.setVisible(True)


    @qtc.pyqtSlot()
    def robot_selection(self):
        if self.rotation_blue_robot.isChecked() == True:
            self.which_robot = "Blue"
            print(self.which_robot)
        elif self.rotation_red_robot.isChecked() == True:
            self.which_robot = "Red"
        else:
            self.which_robot = "Error"

    @qtc.pyqtSlot()
    def mode_state(self):
        if self.planning_tab.currentIndex() == 0:
            self.which_mode = "Calibration"
        elif self.planning_tab.currentIndex() == 1:
            self.which_mode = "B-Scan"
        elif self.planning_tab.currentIndex() == 2:
            self.which_mode = "Linear-Array"
        elif self.planning_tab.currentIndex() == 3:
            self.which_mode = "2D-Array"
        else:
            self.which_mode = "Error"

    
    def proceed_to_measurement_state(self):
        if self.checklist_done == True and self.lineedit_done == True:
            self.checklist_start_measurement.setEnabled(True)
        else:
            self.checklist_start_measurement.setEnabled(False)


    @qtc.pyqtSlot()
    def set_start_point(self):
        self.coordinates_blue = self.read_coordinates_blue()
        self.coordinates_red = self.read_coordinates_red()


    @qtc.pyqtSlot()
    def populate_coordinates_blue(self, coordinates_blue):
        self.setup_blue_x.setValue(coordinates_blue[0])
        self.setup_blue_y.setValue(coordinates_blue[1])
        self.setup_blue_z.setValue(coordinates_blue[2])
        self.setup_blue_r.setValue(coordinates_blue[3])
    
    
    @qtc.pyqtSlot()
    def populate_coordinates_red(self, coordinates_red):
        self.setup_red_x.setValue(coordinates_red[0])
        self.setup_red_y.setValue(coordinates_red[1])
        self.setup_red_z.setValue(coordinates_red[2])
        self.setup_red_r.setValue(coordinates_red[3])

    
    @qtc.pyqtSlot()
    def read_coordinates_blue(self):
        x = self.setup_blue_x.value()
        y = self.setup_blue_y.value()
        z = self.setup_blue_z.value()
        r = self.setup_blue_r.value()

        self.coordinates_blue = [x, y, z, r]
        return self.coordinates_blue


    @qtc.pyqtSlot()
    def read_coordinates_red(self):
        x = self.setup_red_x.value()
        y = self.setup_red_y.value()
        z = self.setup_red_z.value()
        r = self.setup_red_r.value()

        self.coordinates_red = [x, y, z, r]
        return self.coordinates_red


    @qtc.pyqtSlot()
    def load_blue(self):
        robo_message = RobOp.roboter_message(self, network_parameters.tnblue, "C:R:CURRENT_POSITION", "R:C:CURRENT_POSITION")
        self.coordinates_blue = RobOp.message_parser(self, robo_message)
        self.populate_coordinates_blue(self.coordinates_blue)


    @qtc.pyqtSlot()
    def load_red(self):
        robo_message = RobOp.roboter_message(self, network_parameters.tnred, "C:R:CURRENT_POSITION", "R:C:CURRENT_POSITION")
        self.coordinates_red = RobOp.message_parser(self, robo_message)
        self.populate_coordinates_red(self.coordinates_red)


    @qtc.pyqtSlot()
    def goto_blue(self):
        self.coordinates_blue = self.read_coordinates_blue()
        coordinates_message = RobOp.message_assembler(self, self.coordinates_blue)
        robo_message = RobOp.roboter_message_move(self, network_parameters.tnblue, "C:R:GOTO_POSITION", coordinates_message, "R:C:GOTO_POSITION")
        self.coordinates_blue = RobOp.message_parser(self, robo_message)
        self.populate_coordinates_blue(self.coordinates_blue)


    @qtc.pyqtSlot()
    def goto_red(self):
        self.coordinates_red = self.read_coordinates_red()
        coordinates_message = RobOp.message_assembler(self, self.coordinates_red)
        robo_message = RobOp.roboter_message_move(self, network_parameters.tnred, "C:R:GOTO_POSITION", coordinates_message, "R:C:GOTO_POSITION")
        self.coordinates_red = RobOp.message_parser(self, robo_message)
        self.populate_coordinates_red(self.coordinates_red)

    
    @qtc.pyqtSlot()
    def adapt_graph(self):
        self.lin_label.resize(20, 40)

    ## Calculation ## 

    @qtc.pyqtSlot()
    def rotation_calculation(self):
        self.angle_step_size = self.rotation_angle_step_size.value()
        self.total_rotation = self.rotation_total_rotation.value()
        self.rotation_distance = self.rotation_rotation_distance.value()

        self.calibration_rotation_dataframe = RobOp.calibration_calculation(self, self.which_robot, self.angle_step_size, self.total_rotation, self.coordinates_blue, self.coordinates_red)

    #def bscan_calculation(self):
        #self.bscan_dataframe = 

    #def linear_array_calculation(self):
        #self.linear_array_dataframe =

    #def two_d_array_calculation(self):
        #self.two_d_array_dataframe = 


    @qtc.pyqtSlot()
    def save_csv(self):
        filename = "C:/Users/Moritz/Documents/Code/Roboter/new_ui/test.csv"
        #filename = "/Users/julian/Documents/HybridEcho/Roboter/new_ui"
        RobOp.save_to_csv(self, self.calibration_rotation_dataframe, filename)


    @qtc.pyqtSlot()
    def report_progress(self, n):
        ##To do##
        self.status_progressbar.setValue(((i+1)*100)/len(self.calibration_rotation_dataframe))

    @qtc.pyqtSlot()
    def initialize_measurement(self):

        if self.which_mode == "Calibration":
            angle_step_size = self.rotation_angle_step_size.value()
            total_rotation = self.rotation_total_rotation.value()
            rotation_distance = self.rotation_rotation_distance.value()
            #PXIOp.UDP_connection_PXI(self, udp_messages.message_PXI_start + "Test", udp_messages.response_PXI_start  + "Test")
            #PXIOp.UDP_connection_PXI(self,udp_messages.message_PXI_Log_parameter +f"Angle Step [deg] {angle_step_size} \n Total Angle Range [deg] {total_rotation} \n Rotation Distance [cm] {rotation_distance} \n" , udp_messages.response_PXI_Log_parameter)

            self.initialize_measurement_finished.emit(self.calibration_rotation_dataframe)

        elif self.which_mode == "B-Scan":
            self.initialize_measurement_finished.emit(self.bscan_dataframe)
        elif self.which_mode == "Linear-Array":
            self.initialize_measurement_finished.emit(self.linear_array_dataframe)
        elif self.which_mode == "2D-Array":
            self.initialize_measurement_finished.emit(self.two_d_array_dataframe)
        else:
            print("Please select mode.")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow()
    sys.exit(app.exec())