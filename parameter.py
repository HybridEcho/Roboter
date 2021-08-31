import telnetlib
import numpy as np

class network_parameters:
    ip_PXI = "192.168.33.2"
    ip_local_socket = "192.168.33.101"
    port_PXI = 53000
    tnred = telnetlib.Telnet(b"192.168.33.11")
    tnblue = telnetlib.Telnet(b"192.168.33.10")
class udp_messages:
    name_folder = ''
    message_PXI_start="MEAS:NEW:" + "name_folder"
    message_PXI_reached_position="MEAS:START"
    message_PXI_check_measure="MEAS:CHECK_READY"
    message_PXI_end="MEAS:REPORT"
    message_PXI_Log="MEAS:LOG:LOGFILE:"

    response_PXI_start="ACK:MEAS:NEW:" + "name_folder"
    response_PXI_reached_position="ACK:MEAS:START"
    response_PXI_check_measure="ACK:MEAS:CHECK_READY:READY"
    response_PXI_end="ACK:MEAS:REPORT"
    response_PXI_Log="ACK:MEAS:LOG:LOGFILE"

    def set_folder_name(name):
        udp_messages.name_folder = name

class import_csv:
    cMUT_points_np = np.atleast_2d(np.genfromtxt ("cMUT_Points.csv", delimiter=','))
    piezo_points_np = np.atleast_2d(np.genfromtxt ("Piezo_Points.csv", delimiter=','))
    cMUT_points_np_std = np.atleast_2d(np.genfromtxt ("cMUT_Points_std.csv", delimiter=','))
    piezo_points_np_std= np.atleast_2d(np.genfromtxt ("Piezo_Points_std.csv", delimiter=','))
    combined_points_np= np.atleast_2d(np.genfromtxt ("combined_points.csv", delimiter=','))

