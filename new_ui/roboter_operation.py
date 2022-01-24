from PyQt5 import QtCore as qtc
import time
import numpy as np

class RoboterOperation(qtc.QObject):
    def save_status(self):
        print("Hallo Hallo.")
    
    def roboter_message (self, tn_robo, message):
        message=message
        tn_robo.write(message)
        print("send Message")
        if message == "MOV\r\n".encode("ascii"): 
            tn_robo.read_until("Doesntmatter".encode("ascii"), 0.5) #Workaround, um Datenleitung zu resetten (kann eventuell weggelassen werden)
        else:
            print(" ")

    def roboter_feedback(self, tn_robo, exp_feedback_ascii): 
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
            return(error)
        elif "P" in info_from_robo:
            print("P-Schleife")
            message_from_robo = tn_robo.read_until("\n".encode("ascii"), 2.0) 
            message_from_robo = message_from_robo.decode("ascii")
            message_from_robo = message_from_robo.strip("\n""\r")
            print(message_from_robo)
        elif "WRONG" in info_from_robo:
            print(info_from_robo)
            return(info_from_robo)
    
    def roboter_movement_by_csv(self, number_of_measurement, csv_data, tn_robo):
        self.roboter_message(tn_robo, ("MOV\r\n".encode("ascii")))
        print("start Message was send")
        if tn_robo == parameter.network_parameters.tnred :
            message_robo_point_np = np.array([csv_data[number_of_measurement,4], csv_data[number_of_measurement,5], csv_data[number_of_measurement,6], csv_data[number_of_measurement,7]])
            message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
            message_robo_point_string = message_robo_point_prestring.strip('['']')
            print(message_robo_point_string)
        else:
            print("blue on")
            message_robo_point_np = np.array([csv_data[number_of_measurement,0], csv_data[number_of_measurement,1], csv_data[number_of_measurement,2], csv_data[number_of_measurement,3]])
            message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
            message_robo_point_string = message_robo_point_prestring.strip('['']')
            print(message_robo_point_string)
        message_robo_point="P1 = ".encode("ascii") + message_robo_point_string.encode("ascii") + " 0 0 2\r\n".encode("ascii")
        self.roboter_message(tn_robo, message_robo_point)
        print("send point")
        print(message_robo_point)
        print("Point Message was send")
        self.roboter_feedback(tn_robo, "P11=".encode("ascii"))
        time.sleep(0.2)
