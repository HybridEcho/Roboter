import telnetlib
import numpy as np
import pickle


# class network_parameters:
#     ip_PXI = "192.168.33.2"
#     ip_local_socket = "192.168.33.101"
#     port_PXI = 53000
#     tnred = telnetlib.Telnet(b"192.168.33.11")
#     tnblue = telnetlib.Telnet(b"192.168.33.10")
class udp_messages:
    message_PXI_start="MEAS:NEW:"
    message_PXI_reached_position="MEAS:START"
    message_PXI_check_measure="MEAS:CHECK_READY"
    message_PXI_end="MEAS:REPORT"
    message_PXI_Log="MEAS:LOG:LOGFILE:"
    message_PXI_m_mode_start="MEAS:MMODE:START:50:10"
    message_PXI_m_mode_stop="MEAS:MMODE:STOP"
    message_PXI_suture="MEAS:MECHBSCAN:NEW:18"
    message_PXI_tissue="MEAS:MECHBSCAN:NEW:40"
    message_PXI_start_a_scan="MEAS:MECHBSCAN:NOW"

    response_PXI_start="ACK:MEAS:NEW:"
    response_PXI_reached_position="ACK:MEAS:START"
    response_PXI_check_measure="ACK:MEAS:CHECK_READY:READY"
    response_PXI_end="ACK:MEAS:REPORT"
    response_PXI_Log="ACK:MEAS:LOG:LOGFILE"
    response_PXI_m_mode_start="ACK:MEAS:MMODE:START:50:10"
    response_PXI_m_mode_stop="ACK:MEAS:MMODE:STOP"
    response_PXI_suture="ACK:MEAS:MECHBSCAN:NEW:18"
    response_PXI_tissue="ACK:MEAS:MECHBSCAN:NEW:40"
    response_PXI_start_a_scan="ACK:MEAS:MECHBSCAN:NOW"

class import_csv:
    def load_red_points_np():
        red_points_np = np.atleast_2d(np.genfromtxt ("red_Points.csv", delimiter=','))
        return red_points_np
    def load_blue_points_np():
        blue_points_np = np.atleast_2d(np.genfromtxt ("blue_Points.csv", delimiter=','))
        return blue_points_np
    def load_red_points_std_np():
        red_points_np_std = np.atleast_2d(np.genfromtxt ("red_Points_std.csv", delimiter=','))
        return red_points_np_std
    def load_blue_points_std():
        blue_points_np_std= np.atleast_2d(np.genfromtxt ("blue_Points_std.csv", delimiter=','))
        return blue_points_np_std
    def load_combined_points_np():
        combined_points_np= np.atleast_2d(np.genfromtxt ("combined_points.csv", delimiter=','))
        return combined_points_np
    def load_points_suture():
        combined_points_np= np.atleast_2d(np.genfromtxt ("points_suture.csv", delimiter=','))
        return combined_points_np
    def load_points_tissue():
        combined_points_np= np.atleast_2d(np.genfromtxt ("points_tissue.csv", delimiter=','))
        return combined_points_np
    def load_points_robot_out():
        combined_points_np= np.atleast_2d(np.genfromtxt ("robot_out.csv", delimiter=','))
        return combined_points_np
    def load_points_neutral_position():
        combined_points_np= np.atleast_2d(np.genfromtxt ("neutral_position.csv", delimiter=','))
        return combined_points_np
class import_text:
    def load_text(textfile_str):
        textfile_str = textfile_str + ".txt"
        with open(textfile_str, "rb") as myFile:
            dictionary = pickle.load(myFile)
        return dictionary

class gui:
    def drop_down(activity):
        activity= [
        "on",
        "off",
        ]
        return activity