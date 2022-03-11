from PyQt5 import QtCore as qtc
import time
import numpy as np
import pandas as pd
from parameter import network_parameters
import re
import copy

class RoboterOperation(qtc.QObject):
    #def __init__(self):
    #    pass


    def roboter_message(self, tn_robo, message, end_message):
        """Sends message to roboter controller via ethernet

        Parameters
        ----------
        tn_robo : Class with host adress
            Ethernet adress
        message : ASCII
            Command for roboter
        end_message: ASCII
            Message to end conversation
        """
        tn_robo.write(f"{message}\r\n".encode("ascii"))
        #print(message)        
        #print("message sent")
        reply = tn_robo.read_until(f"{end_message}\r\n".encode("ascii"), 10)
        #print("read message")
        return reply


    def roboter_message_move(self, tn_robo, message, coordinates_message, end_message):
        tn_robo.write(f"{message}\r\n".encode("ascii"))
        #print(message)
        #print("message sent")
        movement_message = "P1 = ".encode("ascii") + coordinates_message.encode("ascii") + " 0 0 2\r\n".encode("ascii")
        tn_robo.write(movement_message)
        #print(movement_message)
        #print("coordinates message sent")
        reply = tn_robo.read_until(f"{end_message}\r\n".encode("ascii"), 10)
        #print("read message")
        return reply
        
        
    def message_parser(self, message):
        #print(message)
        message_str = message.decode() # convert byte to string
        data_str_split = message_str.split('P11')[1] # split str by "P11"
        num_values =  re.findall(r'[-+]?(?:\d*\.\d+|\d+)', data_str_split) 
        x = float(num_values[0])
        y = float(num_values[1])
        z = float(num_values[2])
        r = float(num_values[3])
        coordinates = [x, y, z, r]
        return coordinates


    def message_assembler(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]
        r = coordinates[3]
        coordinates_message = f"{x:.2f}" + " " + f"{y:.2f}" + " " + f"{z:.2f}" + " " + f"{r:.2f}"
        return coordinates_message


    def calibration_calculation(self, which_robot, angle_step_size, total_rotation, start_position_blue, start_position_red):
        start_position_calibration_blue = copy.copy(start_position_blue)
        start_position_calibration_red = copy.copy(start_position_red)
        number_of_steps = total_rotation / angle_step_size
        step_array = np.arange(0, total_rotation+angle_step_size, angle_step_size)
        
        if which_robot == "Blue":
            start_position_calibration_blue[3] = start_position_calibration_blue[3] - total_rotation/2
            calibration_array_blue = np.column_stack((start_position_calibration_blue[0] + step_array*0, start_position_calibration_blue[1] + step_array*0, start_position_calibration_blue[2] + step_array*0, start_position_calibration_blue[3] + step_array))
            calibration_array_red = np.tile(start_position_red, (int(number_of_steps+1), 1))
        elif which_robot == "Red":
            start_position_calibration_red[3] = start_position_calibration_red[3] - total_rotation/2
            calibration_array_blue = np.tile(start_position_blue, (int(number_of_steps+1), 1))
            calibration_array_red = np.column_stack((start_position_calibration_red[0] + step_array*0, start_position_calibration_red[1] + step_array*0, start_position_calibration_red[2] + step_array*0, start_position_calibration_red[3] + step_array))
        else:
            print("Error! Please select robot")

        #print(calibration_array_blue)
        #print(calibration_array_red)
        calibration_array = np.concatenate((calibration_array_blue, calibration_array_red), axis=1)
        calibration_dataframe = pd.DataFrame(calibration_array, columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])
        return calibration_dataframe


    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename)


    def set_position_blue(self):
        message = "C:R:GOTO_POSITION"
        tn_robo = "Robo Blue"
        return tn_robo, message


    def set_position_red(self):
        message = "C:R:GOTO_POSITION"
        tn_robo = "Robo Red"
        return tn_robo, message