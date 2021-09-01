#ToDo:
# Bei Current Position die Antowrt des Roboters checken und das Signalwort an den Roboter

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

import move
import parameter

ip_robo_hinten = b"192.168.33.11"
ip_robo_vorne = b"192.168.33.10"


def current_position():
    import parameter
    move.roboter_message(parameter.network_parameters.tnblue,"POINT\r".encode("ascii"))
    print("Blue Robot:")
    move.roboter_feedback(parameter.network_parameters.tnblue, Point)
    move.roboter_message(parameter.network_parameters.tnred,"POINT\r".encode("ascii"))
    print("Red Robot:")
    move.roboter_feedback(parameter.network_parameters.tnred, Point)

    parameter.network_parameters.tnblue.close()
    parameter.network_parameters.tnred.close()

def start_mov():
    move.naming_experiment(parameter.network_parameters) 
    ## Start Robo
    print("starting Roboter...")
    print("blue")
    move.roboter_feedback(parameter.network_parameters.tnblue, "Welcome to RCX340")
    print("red")
    move.roboter_feedback(parameter.network_parameters.tnred, "Welcome to RCX340")
    ## Starting the PXI-System
    print("starting PXI...")
    #move.UDP_connection_PXI(parameter.udp_messages.message_PXI_start, parameter.udp_messages.response_PXI_start)
    print("successsfully started PXI")

    print("start measurement")
    for number_of_measurement in range((len(parameter.import_csv.combined_points_np)+1)):
        print("Blue")
        move.roboter_movement_by_csv(number_of_measurement,parameter.import_csv.combined_points_np, parameter.network_parameters.tnblue)
        print("red")
        move.roboter_movement_by_csv(number_of_measurement,parameter.import_csv.combined_points_np, parameter.network_parameters.tnred)
        time.sleep(0.2)

        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_reached_position, parameter.udp_messages.response_PXI_reached_position)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_Log, parameter.udp_messages.response_PXI_Log)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_check_measure, parameter.udp_messages.response_PXI_check_measure)

    parameter.network_parameters.tnblue.close()
    parameter.network_parameters.tnred.close()
    move.UDP_connection_PXI(parameter.udp_messages.message_PXI_end, parameter.udp_messages.response_PXI_end)
    print("End of Experiment")

def reset_rob():
    print("Reseting Roboter:")

    while "WRONG STARTING COMMAND" in move.roboter_feedback(parameter.network_parameters.tnblue) and "WRONG STARTING COMMAND" in move.roboter_feedback(parameter.network_parameters.tnred):
        print("Try reset blue")
        move.roboter_message(parameter.network_parameters.tnblue, "RESET\r\n".encode("ascii"))
        print("Try reset red")
        move.roboter_message(parameter.network_parameters.tnred, "RESET\r\n".encode("ascii"))
        #move.roboter_feedback(parameter.network_parameters.tnblue)
        #move.roboter_feedback(parameter.network_parameters.tnred)
        print("...")

    print("Reset complete!")

def point_calc():
    print("opening")
    subprocess.run(["python","linear_2d_planning.py"])
    print("closed")

def bscan_piezo():
    print("opening")
    subprocess.run(["python","b_scan_piezo.py"])
    print("closed")

def bscan_both():
    print("opening")
    subprocess.run(["python","b_scan_both.py"])
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

button5 = tk.Button(text='b Scan by Piezo', command= bscan)
canvas_start_points.create_window(150, 250, window=button5)

standard.mainloop()
