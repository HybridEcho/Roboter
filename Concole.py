#ToDo:
# die Planungstools modularisieren

import importlib
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
    move.roboter_message(parameter.network_parameters.tnblue,"POINT\r".encode("ascii"))
    print("Blue Robot:")
    move.roboter_feedback(parameter.network_parameters.tnblue, "P20=\r".encode("ascii"))
    move.roboter_message(parameter.network_parameters.tnred,"POINT\r".encode("ascii"))
    print("Red Robot:")
    move.roboter_feedback(parameter.network_parameters.tnred, "P20=".encode("ascii"))

def start_mov():
    ## Setting Foldername
    foldername=input(":")
    message_PXI_start=parameter.udp_messages.message_PXI_start+foldername
    response_PXI_start=parameter.udp_messages.response_PXI_start+foldername
    ## Start Robo
    print("starting Roboter...")
    print("blue")
    move.roboter_feedback(parameter.network_parameters.tnblue, "Welcome to RCX340".encode("ascii"))
    print("red")
    move.roboter_feedback(parameter.network_parameters.tnred, "Welcome to RCX340".encode("ascii"))
    ## Starting the PXI-System
    print("starting PXI...")
    move.UDP_connection_PXI(message_PXI_start, response_PXI_start)
    print("successsfully started PXI")

    print("start measurement")
    for number_of_measurement in range((len(parameter.import_csv.load_combined_points_np()))):
        print("Measurement:", number_of_measurement+1, "of", (len(parameter.import_csv.load_combined_points_np())))
        print("  red")
        move.roboter_movement_by_csv(number_of_measurement,parameter.import_csv.load_combined_points_np(), parameter.network_parameters.tnred)
        print("  Blue")
        move.roboter_movement_by_csv(number_of_measurement,parameter.import_csv.load_combined_points_np(), parameter.network_parameters.tnblue)
        time.sleep(0.2)

        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_reached_position, parameter.udp_messages.response_PXI_reached_position)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_Log, parameter.udp_messages.response_PXI_Log)
        move.UDP_connection_PXI(parameter.udp_messages.message_PXI_check_measure, parameter.udp_messages.response_PXI_check_measure)

    move.UDP_connection_PXI(parameter.udp_messages.message_PXI_end, parameter.udp_messages.response_PXI_end)
    print("End of Experiment")

def reset_rob():
    print("Reseting Roboter:")
    info_from_robo_blue="0"
    while "WRONG STARTING COMMAND" not in info_from_robo_blue:
        print("Try reset blue")
        move.roboter_message(parameter.network_parameters.tnblue, "RESET\r\n".encode("ascii"))
        info_from_robo_blue=move.roboter_feedback(parameter.network_parameters.tnblue, "WRONG STARTING COMMAND".encode("ascii"))
        print("...")
    info_from_robo_red="0"
    while "WRONG STARTING COMMAND" not in info_from_robo_red:
        print("Try reset red")
        move.roboter_message(parameter.network_parameters.tnred, "RESET\r\n".encode("ascii"))
        info_from_robo_red=move.roboter_feedback(parameter.network_parameters.tnred, "WRONG STARTING COMMAND".encode("ascii"))
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

button5 = tk.Button(text='b Scan by Piezo', command= bscan_piezo)
canvas_start_points.create_window(150, 250, window=button5)

button6 = tk.Button(text='b Scan both', command= bscan_both)
canvas_start_points.create_window(300, 250, window=button6)

standard.mainloop()
