from PyQt5 import QtCore as qtc
import time
import numpy as np
import socket
import parameter

class PXIOperation(qtc.QObject):
    def status(self):
        print("Hallo Welt.")

    def UDP_connection_PXI (self, message, response):
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        answer_PXI = ""
        while answer_PXI != response.encode("UTF-8"):
            s.sendto((message.encode("ascii")), (parameter.network_parameters.ip_PXI, parameter.network_parameters.port_PXI))
            try:
                s.settimeout(100)
                daten, addr = s.recvfrom(1024)
                answer_PXI = daten
                nice_output_PXI = daten
                print("    Status PXI: " + str(nice_output_PXI) )
            except:
                print("PXI did not echo to " + message + ", will try again")
            if (time.time() - start_time > 10):
                print("PXI did not echo after 10s of repeated", message, "sending, Programm ende")
                exit()

    def message_pxi_robo_points(self, number_of_measurement, csv_data):
        message_robo_point_np = np.array([csv_data[number_of_measurement,4], csv_data[number_of_measurement,5], csv_data[number_of_measurement,6], csv_data[number_of_measurement,7]])
        message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator='\t', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
        message_robo_point_string = message_robo_point_prestring.strip('['']')
        return message_robo_point_string