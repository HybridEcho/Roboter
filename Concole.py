#ToDo:

import importlib
import tkinter as tk
from tkinter.constants import RAISED, SUNKEN
from tkinter.font import BOLD, ITALIC
from mpl_toolkits import mplot3d
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import telnetlib #kann eventuell weg
import subprocess
import time
import socket 
import parameter

############## gui functions################

def activity_a_scan(scan_activity):
    if scan_activity == "on":
        a_scan_info_red_text.configure(text="on",background="green")
        a_scan_info_blue_text.configure(text="on",background="green")
    elif scan_activity == "off":
        a_scan_info_red_text.configure(text="off",background="yellow")
        a_scan_info_blue_text.configure(text="off",background="yellow")

def activity_robot_red(activity):
    if activity == "on":
        roboter_info_text_red.configure(text="on",background="green")
    elif activity == "off":
        roboter_info_text_red.configure(text="off",background="yellow")

def activity_robot_blue(activity):
    if activity == "on":
        roboter_info_text_blue.configure(text="on",background="green")
    elif activity == "off":
        roboter_info_text_blue.configure(text="off",background="yellow")

###############interactive functions####################################


def UDP_connection_PXI (message, response):
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

def roboter_message (tn_robo, message):
    message=message
    tn_robo.write(message)
    print("send Message")
    if message == "MOV\r\n".encode("ascii"): 
        tn_robo.read_until("Doesntmatter".encode("ascii"), 0.5) #Workaround, um Datenleitung zu resetten (kann eventuell weggelassen werden)
    else:
        print(" ")
        
def roboter_feedback(tn_robo, exp_feedback_ascii): 
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


def roboter_movement_by_csv(number_of_measurement, csv_data, tn_robo):
    roboter_message(tn_robo, ("MOV\r\n".encode("ascii")))
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
    roboter_message(tn_robo, message_robo_point)
    print("send point")
    print(message_robo_point)
    print("Point Message was send")
    roboter_feedback(tn_robo, "P11=".encode("ascii"))
    time.sleep(0.2)

def message_pxi_robo_points(number_of_measurement, csv_data):
    message_robo_point_np = np.array([csv_data[number_of_measurement,4], csv_data[number_of_measurement,5], csv_data[number_of_measurement,6], csv_data[number_of_measurement,7]])
    message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator='\t', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
    message_robo_point_string = message_robo_point_prestring.strip('['']')
    return message_robo_point_string

def mech_b_scan(csv_data, standard):
    start_time=time.time()
    for number_of_measurement in range((len(csv_data))):
        print("Measurement:", number_of_measurement+1, "of", (len(csv_data)))
        print("starting Roboter...")
        activity_robot_blue("on")
        standard.update()                                       #was macht dieser Abschnitt?
        roboter_movement_by_csv(number_of_measurement,csv_data, parameter.network_parameters.tnblue)
        activity_robot_red("on")
        activity_robot_blue("off")
        standard.update()
        roboter_movement_by_csv(number_of_measurement,csv_data, parameter.network_parameters.tnred)
        activity_robot_red("off")
        activity_a_scan("on")
        standard.update()
        time.sleep(0.2)
        UDP_connection_PXI(parameter.udp_messages.message_PXI_start_a_scan , parameter.udp_messages.response_PXI_start_a_scan)
        activity_a_scan("off")
        standard.update()
    end_time=time.time()
    print(end_time-start_time)

######### button functions##############################################
def reset_rob():
    print("Reseting Roboter:")
    roboter_feedback(parameter.network_parameters.tnblue, "WRONG STARTING COMMAND".encode("ascii"))
    roboter_feedback(parameter.network_parameters.tnred, "WRONG STARTING COMMAND".encode("ascii"))
    info_from_robo_blue="0"
    while "WRONG STARTING COMMAND" not in info_from_robo_blue:
        print("Try reset blue")
        roboter_message(parameter.network_parameters.tnblue, "RESET\r\n".encode("ascii"))
        info_from_robo_blue=roboter_feedback(parameter.network_parameters.tnblue, "WRONG STARTING COMMAND".encode("ascii"))
        print("...")
    info_from_robo_red="0"
    while "WRONG STARTING COMMAND" not in info_from_robo_red:
        print("Try reset red")
        roboter_message(parameter.network_parameters.tnred, "RESET\r\n".encode("ascii"))
        info_from_robo_red=roboter_feedback(parameter.network_parameters.tnred, "WRONG STARTING COMMAND".encode("ascii"))
        print("...")

    print("Reset complete!")

def start_m_mode():
    activity_a_scan("on")
    UDP_connection_PXI(parameter.udp_messages.message_PXI_m_mode_start, parameter.udp_messages.response_PXI_m_mode_start)

def stop_m_mode():
    activity_a_scan("off")
    standard.update()
    UDP_connection_PXI(parameter.udp_messages.message_PXI_m_mode_stop, parameter.udp_messages.response_PXI_m_mode_stop)

def suture():
    UDP_connection_PXI(parameter.udp_messages.message_PXI_suture , parameter.udp_messages.response_PXI_suture)
    mech_b_scan(parameter.import_csv.load_points_suture(), standard)
    activity_robot_blue("on")
    standard.update()
    roboter_movement_by_csv(0,parameter.import_csv.load_points_neutral_position(), parameter.network_parameters.tnblue)
    activity_robot_red("on")
    activity_robot_blue("off")
    standard.update()
    roboter_movement_by_csv(0,parameter.import_csv.load_points_neutral_position(), parameter.network_parameters.tnred)
    activity_robot_red("off")
    standard.update()


def tissue():
    UDP_connection_PXI(parameter.udp_messages.message_PXI_tissue , parameter.udp_messages.response_PXI_tissue)
    mech_b_scan(parameter.import_csv.load_points_tissue(), standard)
    activity_robot_blue("on")
    standard.update()
    # roboter_movement_by_csv(0,parameter.import_csv.load_points_neutral_position(), parameter.network_parameters.tnblue)
    # activity_robot_red("on")
    activity_robot_blue("off")
    standard.update()
    # roboter_movement_by_csv(0,parameter.import_csv.load_points_neutral_position(), parameter.network_parameters.tnred)
    activity_robot_red("off")
    standard.update()

def get_robot_out():
    activity_robot_blue("on")
    standard.update()
    roboter_movement_by_csv(0,parameter.import_csv.load_points_robot_out(), parameter.network_parameters.tnblue)
    activity_robot_red("on")
    activity_robot_blue("off")
    standard.update()
    roboter_movement_by_csv(0,parameter.import_csv.load_points_robot_out(), parameter.network_parameters.tnred)
    activity_robot_red("off")
    standard.update()

standard= tk.Tk()
#general Window settings
canvas_start_points = tk.Canvas(standard, width = 1400, height = 800, background="white")
canvas_start_points.pack()

label_m_mode = tk.Label(standard, text='HybridEcho', font=('helvetica', 30, BOLD), background="white")
canvas_start_points.create_window(650, 50, window=label_m_mode)

##### right upper side
button_advanced_settings = tk.Button(text='Advanced Settings', font=('helvetica', 16), borderwidth=7, command= start_m_mode, width=15, height=2)
canvas_start_points.create_window(1025, 175, window=button_advanced_settings)

button_robot_out = tk.Button(text='Safe Postion', command= get_robot_out, font=('helvetica', 16), borderwidth=3)
canvas_start_points.create_window(900, 275, window=button_robot_out)

button_reset_robot = tk.Button(text='Reset Robot', command= reset_rob, font=('helvetica', 16), borderwidth=3)
canvas_start_points.create_window(1150, 275, window=button_reset_robot)


# label_robo_control = tk.Label(standard, text='Roboter Controle', background="white", font=('helvetica', 22, BOLD))
# canvas_start_points.create_window(950, 150, window=label_robo_control)

# label_red = tk.Label(standard, text='Piezo Roboter', background="white", font=('helvetica', 16))
# canvas_start_points.create_window(800, 190, window=label_red)
# activity_red_str = tk.StringVar(standard)
# activity_red_str.set(parameter.gui.drop_down("red_activity")[0])
# activity_red = tk.OptionMenu(standard, activity_red_str, *parameter.gui.drop_down("red_activity"))
# activity_red.config(width=10, background="white",font=('helvetica', 16))
# canvas_start_points.create_window(1050, 190, window=activity_red)

# label_red = tk.Label(standard, text='Hybrid Roboter',background="white", font=('helvetica', 16))
# canvas_start_points.create_window(800, 240, window=label_red)
# activity_blue_str = tk.StringVar(standard)
# activity_blue_str.set(parameter.gui.drop_down("red_activity")[0])
# activity_blue = tk.OptionMenu(standard, activity_blue_str, *parameter.gui.drop_down("red_activity"))
# activity_blue.config(width=10,background="white", font=('helvetica', 16))
# canvas_start_points.create_window(1050, 240, window=activity_blue)

##### right lower side

label_activity_feedback = tk.Label(standard, text='Status', font=('helvetica', 22, BOLD), background="white")
canvas_start_points.create_window(1025, 380, window=label_activity_feedback)

label_infos_activity_red=tk.Label(standard, text="Hybrid Robot", background="WHITE", font=('helvetica', 16))
canvas_start_points.create_window(800, 475, window=label_infos_activity_red)
a_scan_info_titel=tk.Label(standard, text="Servo", background="WHITE", font=('helvetica', 16))
canvas_start_points.create_window(1075, 425, window=a_scan_info_titel)
a_scan_info_titel=tk.Label(standard, text="Ultrasound", background="WHITE", font=('helvetica', 16))
canvas_start_points.create_window(950, 425, window=a_scan_info_titel)

a_scan_info_red_text=tk.Label(standard, text="starting", background="gray", font=('helvetica', 16), relief=SUNKEN, height=2, width=7)
canvas_start_points.create_window(950, 475, window=a_scan_info_red_text)
roboter_info_text_red=tk.Label(standard, text="starting", background="gray", font=('helvetica', 16), relief=SUNKEN, height=2, width=7)
canvas_start_points.create_window(1075, 475, window=roboter_info_text_red)


label_infos_activity_blue=tk.Label(standard, text="Piezo Robot", background="WHITE", font=('helvetica', 16))
canvas_start_points.create_window(800, 535, window=label_infos_activity_blue)
a_scan_info_blue_text=tk.Label(standard, text="starting", background="gray", font=('helvetica', 16), relief=SUNKEN, height=2, width=7)
canvas_start_points.create_window(950, 535, window=a_scan_info_blue_text)
roboter_info_text_blue=tk.Label(standard, text="starting", background="gray", font=('helvetica', 16), relief=SUNKEN, height=2, width=7)
canvas_start_points.create_window(1075, 535, window=roboter_info_text_blue)

########### left side
label_mech_bscan = tk.Label(standard, text='Mechanical B-Scans', font=('helvetica', 22, BOLD), background="white")
canvas_start_points.create_window(235, 150, window=label_mech_bscan)
button_suture = tk.Button(text='Wire Phantom',  font=('helvetica', 16), borderwidth=7, command= suture, width=15, height=2)
canvas_start_points.create_window(350, 250, window=button_suture)
button_tissue = tk.Button(text='Tissue Model', font=('helvetica', 16), borderwidth=7, command= tissue, width=15, height=2)
canvas_start_points.create_window(120, 250, window=button_tissue)

label_m_mode = tk.Label(standard, text='M-Mode', font=('helvetica', 22, BOLD), background="white")
canvas_start_points.create_window(235, 400, window=label_m_mode)
button_start_m_mode = tk.Button(text='Start', font=('helvetica', 16), borderwidth=7, command= start_m_mode, width=15, height=2)
canvas_start_points.create_window(120, 500, window=button_start_m_mode)
button_stop_m_mode = tk.Button(text='Stop',  font=('helvetica', 16), borderwidth=7, command= stop_m_mode, width=15, height=2,)
canvas_start_points.create_window(350, 500, window=button_stop_m_mode)

standard.mainloop()
