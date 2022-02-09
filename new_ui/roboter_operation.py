from PyQt5 import QtCore as qtc
import time
import numpy as np
import pandas as pd
#from parameter import network_parameters

class RoboterOperation(qtc.QObject):
    def __init__(self):
        self.position_robo_blue = np.array([1])
    
    

    def dev_roboter_message(self, tn_robo, dev_message):
        print(tn_robo + "---" + dev_message)

    def dev_roboter_feedback(self):
        tn_robo = input()
        dev_feedback_message = input()
        dev_feedback = tn_robo + "---" + dev_feedback_message
        return dev_feedback

    # def roboter_message(self, tn_robo, message):
    #     """Sends message to roboter controller via ethernet

    #     Parameters
    #     ----------
    #     tn_robo : Class with host adress
    #         Ethernet adress
    #     message : ASCII
    #         Command for roboter
    #     """
    #     message=message  #warum nochmal assignen?
    #     tn_robo.write(message)
    #     print("send message")
    #     if message == "MOV\r\n".encode("ascii"): 
    #         tn_robo.read_until("Doesntmatter".encode("ascii"), 0.5) #Workaround, um Datenleitung zu resetten (kann eventuell weggelassen werden)
    #     else:
    #         print(" ")

    # def roboter_feedback(self, tn_robo, exp_feedback_ascii):
    #     """Receives feedback of roboter controller via ethernet

    #     Parameters
    #     ----------
    #     tn_robo : Class with host adress
    #         Ethernet adress
    #     exp_feedback_ascii : [type]
    #         [description]
    #     """
    #     info_from_robo_ascii = tn_robo.read_until(exp_feedback_ascii, 10.0) #10 Sekunden Wartezeit
    #     info_from_robo = info_from_robo_ascii.decode("ascii")
    #     info_from_robo = str(info_from_robo)
    #     exp_feedback = exp_feedback_ascii.decode("ascii")
    #     exp_feedback =str(exp_feedback)
    #     if exp_feedback not in info_from_robo:
    #         print("Error-Schleife")
    #         print(info_from_robo)
    #         error = tn_robo.read_until("doesntmatter".encode("ascii"), 3.0) #Workaround, auf Fehler warten
    #         print(error)
    #         return error
    #     elif "P" in info_from_robo:
    #         print("P-Schleife")
    #         message_from_robo = tn_robo.read_until("\n".encode("ascii"), 2.0) 
    #         message_from_robo = message_from_robo.decode("ascii")
    #         message_from_robo = message_from_robo.strip("\n""\r")
    #         print(message_from_robo)
    #     elif "WRONG" in info_from_robo:
    #         print(info_from_robo)
    #         return info_from_robo

    def measurement_execution(self, dataframe):
        for i in dataframe.index:
            print(dataframe["Blue_X"][i], dataframe["Blue_Y"][i], dataframe["Blue_Z"][i], dataframe["Blue_R"][i])
        

    def message_parser(self, message):
        x = float(message[0:6])
        y = float(message[7:13])
        z = float(message[14:20])
        r = float(message[21:27])

        coordinates = np.array([x, y, z, r])

        return coordinates


    def message_assembler(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]
        r = coordinates[3]
        message = str(x) + " " + str(y) + " " + str(z) + " " + str(r)
        return message


    def calibration_calculation(angle_step_size, total_rotation, start_position_blue, start_position_red):
        start_position_calibration_blue = start_position_blue
        start_position_calibration_red = start_position_red
        start_position_calibration_blue[3] = start_position_calibration_blue[3] - total_rotation/2
        number_of_steps = total_rotation / angle_step_size
        step_blue = np.arange(0, number_of_steps+1, angle_step_size)
        calibration_array_blue = np.column_stack((start_position_calibration_blue[0] + step_blue*0, start_position_calibration_blue[1] + step_blue*0, start_position_calibration_blue[2] + step_blue*0, np.round(start_position_calibration_blue[3] + step_blue, 3)))
        calibration_array_red = np.tile(start_position_calibration_red, (int(number_of_steps+1), 1))
        calibration_array = np.concatenate((calibration_array_blue, calibration_array_red), axis=1)
        calibration_dataframe = pd.DataFrame(calibration_array, columns = ["Blue_X","Blue_Y","Blue_Z", "Blue_R", "Red_X","Red_Y","Red_Z", "Red_R"])
        return calibration_dataframe



    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename)


    def servo_blue_on(self):
        message = "C:R:SERVO_ON"
        tn_robo = "Robo Blue"
        return tn_robo, message
    
    def servo_blue_off(self):
        message = "C:R:SERVO_OFF"
        tn_robo = "Robo Blue"
        return tn_robo, message

    def servo_red_on(self):
        message = "C:R:SERVO_ON"
        tn_robo = "Robo Red"
        return tn_robo, message
    
    def servo_red_off(self):
        message = "C:R:SERVO_OFF"
        tn_robo = "Robo Red"
        return tn_robo, message

    def get_position_blue(self):
        message = "C:R:CURRENT_POSITION"
        tn_robo = "Robo Blue"
        return tn_robo, message

    def get_position_red(self):
        message = "C:R:CURRENT_POSITION"
        tn_robo = "Robo Red"
        return tn_robo, message

    def set_position_blue(self):
        message = "C:R:GOTO_POSITION"
        tn_robo = "Robo Blue"
        return tn_robo, message

    def set_position_red(self):
        message = "C:R:GOTO_POSITION"
        tn_robo = "Robo Red"
        return tn_robo, message
    
    # def get_position_blue(self):
    #     self.roboter_message(network_parameters.tnblue, ("C:RB:CURRENT_POSITION\r\n".encode("ascii")))
    #     self.roboter_feedback(network_parameters.tnblue, ("RB:C:END_MESSAGE".encode("ascii")))
    #     self.start_position_blue = 1
    #     return self.start_position_blue

    # def get_position_red(self):
    #     self.roboter_message(network_parameters.tnred, ("C:RR:CURRENT_POSITION\r\n".encode("ascii")))
    #     self.roboter_feedback(network_parameters.tnred, ("RR:C:END_MESSAGE".encode("ascii")))
    #     self.start_position_red = 1
    #     return self.start_position_red

    # def set_position_blue(self):


    # def set_position_red(self):

    

    

    
    # def roboter_movement_by_csv(self, number_of_measurement, csv_data, tn_robo):
    #     self.roboter_message(tn_robo, ("MOV\r\n".encode("ascii")))
    #     print("start Message was send")
    #     if tn_robo == network_parameters.tnred :
    #         message_robo_point_np = np.array([csv_data[number_of_measurement,4], csv_data[number_of_measurement,5], csv_data[number_of_measurement,6], csv_data[number_of_measurement,7]])
    #         message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
    #         message_robo_point_string = message_robo_point_prestring.strip('['']')
    #         print(message_robo_point_string)
    #     else:
    #         print("blue on")
    #         message_robo_point_np = np.array([csv_data[number_of_measurement,0], csv_data[number_of_measurement,1], csv_data[number_of_measurement,2], csv_data[number_of_measurement,3]])
    #         message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
    #         message_robo_point_string = message_robo_point_prestring.strip('['']')
    #         print(message_robo_point_string)
    #     message_robo_point="P1 = ".encode("ascii") + message_robo_point_string.encode("ascii") + " 0 0 2\r\n".encode("ascii")
    #     self.roboter_message(tn_robo, message_robo_point)
    #     print("send point")
    #     print(message_robo_point)
    #     print("Point Message was send")
    #     self.roboter_feedback(tn_robo, "P11=".encode("ascii"))
    #     time.sleep(0.2)

