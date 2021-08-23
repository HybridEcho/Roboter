import tkinter as tk
from mpl_toolkits import mplot3d
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import telnetlib
import subprocess
import sys
import time
import socket 

import Move as move
import parameter

ip_robo_hinten = b"192.168.33.11"
ip_robo_vorne = b"192.168.33.10"



def current_position():
    Meas_where="POINT\r".encode("ascii")

    tnblue = telnetlib.Telnet(ip_robo_vorne)
    tnred = telnetlib.Telnet(ip_robo_hinten)

    tnblue.write(Meas_where)
    tnred.write(Meas_where)

    current_position_vorne = tnblue.read_very_eager()
    current_position_hinten = tnred.read_very_eager()
    current_position_vorne = current_position_vorne.decode("ascii")
    current_position_hinten = current_position_hinten.decode("ascii")

    print("Robo vorne" + current_position_vorne)
    print("Robo hinten" + current_position_hinten)

    tnblue.close()
    tnred.close()

def start_mov():
    move.defining_connections(parameter.network_parameters)    

    ## Starting the PXI-System
    print("starting Roboter...")
    move.starting_RCX_move(parameter.network_parameters.tnblue, parameter.network_parameters.tnred)
    print("successsfully started Roboter")
    ## Starting the PXI-System
    print("starting PXI...")
    move.UDP_connection_PXI(parameter.udp_messages.message_PXI_start, parameter.udp_messages.response_PXI_start)
    print("successsfully started PXI")

    print("start measurement")
    for number_of_measurement in range((len(csv_data)+1)):
        move.roboter_movement_by_csv(number_of_measurement,parameter.import_csv.combined_points_np, parameter.network_parameters.tnblue, parameter.network_parameters.tnred)
        move.roboter_confirmation_position(parameter.network_parameters.tnblue, parameter.network_parameters.tnred)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_reached_position, parameter.udp_messages.response_PXI_reached_position)
        move.UDP_connection_PXI(PXI_LOG, PXI_LOG)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_check_measure, parameter.udp_messages.response_PXI_check_measure)
        parameter.network_parameters.tnred.write("0\r\n".encode("ascii"))
        parameter.network_parameters.tnblue.write("0\r\n".encode("ascii"))




def reset_rob():
    print("Reseting Roboter:")

    tnblue = telnetlib.Telnet(ip_robo_vorne)
    tnred = telnetlib.Telnet(ip_robo_hinten)

    meas_rob_vorne = "0"
    meas_rob_hinten = "0"

    while meas_rob_vorne != "WRONG STARTING COMMAND" and meas_rob_hinten != "WRONG STARTING COMMAND":
        Meas_reset="RESET\r\n".encode("ascii")
        tnblue.write(Meas_reset)
        tnred.write(Meas_reset)

        meas_rob_vorne = tnblue.read_until ("WRONG STARTING COMMAND".encode("ascii"), 0.2)
        meas_rob_vorne = meas_rob_vorne.decode("ascii")
        meas_rob_vorne = meas_rob_vorne.strip("\n""\r")

        meas_rob_hinten = tnblue.read_until ("WRONG STARTING COMMAND".encode("ascii"), 0.2)
        meas_rob_hinten = meas_rob_hinten.decode("ascii")
        meas_rob_hinten = meas_rob_hinten.strip("\n""\r")
        print("...")
    
    tnred.close()
    tnblue.close()
    print("Reset complete!")
def point_calc():
    print("opening")
    subprocess.run(["python","linear_2d_planning.py"])
    print("closed")



standard= tk.Tk()
#general Window settings
canvas_start_points = tk.Canvas(standard, width = 600, height = 600)
canvas_start_points.pack()

button1 = tk.Button(text='current position', command= current_position)
canvas_start_points.create_window(300, 400, window=button1)

button2 = tk.Button(text='start movement', command= start_mov)
canvas_start_points.create_window(150, 400, window=button2)

button3 = tk.Button(text='reset', command= reset_rob)
canvas_start_points.create_window(150, 350, window=button3)

button4 = tk.Button(text='Point Calc', command= point_calc)
canvas_start_points.create_window(150, 300, window=button4)

standard.mainloop()
