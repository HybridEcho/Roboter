from PyQt5 import QtCore as qtc
import time
import numpy as np
import pandas as pd
from parameter import network_parameters
import re

class RoboterOperation(qtc.QObject):
    def __init__(self):
        pass
    
    
    def dev_roboter_message(self, tn_robo, dev_message):
        print(tn_robo + "---" + dev_message)


    def dev_roboter_feedback(self):
        tn_robo = input()
        dev_feedback_message = input()
        dev_feedback = tn_robo + "---" + dev_feedback_message
        return dev_feedback


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
        print(message)        
        print("message sent")
        reply = tn_robo.read_until(f"{end_message}\r\n".encode("ascii"), 10)
        print("read message")
        return reply


    def roboter_message_move(self, tn_robo, message, coordinates_message, end_message):
        tn_robo.write(f"{message}\r\n".encode("ascii"))
        print(message)
        print("message sent")
        movement_message = "P1 = ".encode("ascii") + coordinates_message.encode("ascii") + " 0 0 2\r\n".encode("ascii")
        tn_robo.write(movement_message)
        print(movement_message)
        print("coordinates message sent")
        reply = tn_robo.read_until(f"{end_message}\r\n".encode("ascii"), 10)
        print("read message")
        return reply
        

    def roboter_feedback(self, tn_robo, exp_feedback_ascii):
        """Receives feedback of roboter controller via ethernet

        Parameters
        ----------
        tn_robo : Class with host adress
            Ethernet adress
        exp_feedback_ascii : [type]
            [description]
        """
        info_from_robo_ascii = tn_robo.read_until(exp_feedback_ascii, 10.0) #10 Sekunden Wartezeit
        info_from_robo = info_from_robo_ascii.decode("ascii")
        info_from_robo = str(info_from_robo)
        exp_feedback = exp_feedback_ascii.decode("ascii")
        exp_feedback =str(exp_feedback)
        if exp_feedback not in info_from_robo:
            print("Error-Schleife")
            print(info_from_robo)
            error = tn_robo.read_until("doesntmatter".encode("ascii"), 3.0) #Workaround, auf Fehler warten
            print(error)
            return error
        elif "P" in info_from_robo:
            print("P-Schleife")
            message_from_robo = tn_robo.read_until("\n".encode("ascii"), 2.0) 
            message_from_robo = message_from_robo.decode("ascii")
            message_from_robo = message_from_robo.strip("\n""\r")
            print(message_from_robo)
        elif "WRONG" in info_from_robo:
            print(info_from_robo)
            return info_from_robo

    def measurement_execution(self, dataframe):
        for i in dataframe.index:
            print(dataframe["Blue_X"][i], dataframe["Blue_Y"][i], dataframe["Blue_Z"][i], dataframe["Blue_R"][i])
        

    def message_parser(self, message):
        print(message)
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


    def calibration_calculation(angle_step_size, total_rotation, start_position_blue, start_position_red):
        start_position_calibration_blue = start_position_blue
        start_position_calibration_red = start_position_red
        start_position_calibration_blue[3] = start_position_calibration_blue[3] - total_rotation/2
        number_of_steps = total_rotation / angle_step_size
        step_blue = np.arange(0, total_rotation+angle_step_size, angle_step_size)
        #calibration_array_blue = np.column_stack((start_position_calibration_blue[0] + step_blue*0, start_position_calibration_blue[1] + step_blue*0, start_position_calibration_blue[2] + step_blue*0, np.round(start_position_calibration_blue[3] + step_blue, 3)))
        calibration_array_blue = np.column_stack((start_position_calibration_blue[0] + step_blue*0, start_position_calibration_blue[1] + step_blue*0, start_position_calibration_blue[2] + step_blue*0, start_position_calibration_blue[3] + step_blue))
        calibration_array_red = np.tile(start_position_calibration_red, (int(number_of_steps+1), 1))
        print(calibration_array_blue)
        print(calibration_array_red)
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