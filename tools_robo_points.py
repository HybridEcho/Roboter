import importlib
from os import read
import tkinter as tk
import numpy as np
from mpl_toolkits import mplot3d
from numpy import genfromtxt
import matplotlib.pyplot as plt
import math
import parameter
import importlib

###combining csv files##################
def adding_a_line_to_combined_np(number_of_red_measurement, number_of_blue_measurement, combined_np):
    red = np.array([[parameter.import_csv.load_red_points_np()[number_of_red_measurement,0], parameter.import_csv.load_red_points_np()[number_of_red_measurement,1], parameter.import_csv.load_red_points_np()[number_of_red_measurement,2], parameter.import_csv.load_red_points_np()[number_of_red_measurement,3]]])
    blue = np.array([[parameter.import_csv.load_blue_points_np()[number_of_blue_measurement,0], parameter.import_csv.load_blue_points_np()[number_of_blue_measurement,1], parameter.import_csv.load_blue_points_np()[number_of_blue_measurement,2], parameter.import_csv.load_blue_points_np()[number_of_blue_measurement,3]]])
    combined= np.concatenate((blue, red), axis=1)
    print("combined")
    print(combined)
    print("combined_np")
    print(combined_np)
    combined_np= np.concatenate((combined_np, combined), axis=0)
    print("adding_line Zeile 18")
    print(combined_np)
    return combined_np

def combining_line_by_line():
    combined_np=np.array([[]]).reshape(0,8)
    for number_of_blue_measurement in range((len(parameter.import_csv.load_blue_points_np()))):
        print(range((len(parameter.import_csv.load_blue_points_np()))))
        print(number_of_blue_measurement)
        number_of_red_measurement = number_of_blue_measurement
        combined_np = adding_a_line_to_combined_np(number_of_red_measurement, number_of_blue_measurement, combined_np)
        print("combining line_by_line: Zeile 26")
        print(combined_np)
    np.savetxt("Combined_Points.csv", combined_np, delimiter=",")
    print(combined_np)

def combining_all():
    combined_np=np.array([[]]).reshape(0,8)
    for number_of_blue_measurement in range((len(parameter.import_csv.load_blue_points_np()))):
        for number_of_red_measurement in range((len(parameter.import_csv.load_red_points_np()))):
            combined_np = adding_a_line_to_combined_np(number_of_red_measurement, number_of_blue_measurement, combined_np)
    print(combined_np)
    np.savetxt("Combined_Points.csv", combined_np, delimiter=",")

########## generation of csv #################

def calculat_np(name_of_csv, starting_point, x_pitch, elements_in_x, y_pitch, elements_in_y, z_pitch, elements_in_z, r_pitch, elements_in_r):
    name_of_csv = name_of_csv + ".csv"

    # define startposition and stepsize
    step_size_x = np.array([[x_pitch, 0, 0, 0]])
    step_size_y = np.array([[0, y_pitch, 0, 0]])
    step_size_z = np.array([[0, 0, z_pitch, 0]])
    step_size_r = np.array([[0, 0, 0, r_pitch]])

    #define starting array
    points_np = np.array([[]]).reshape(0,4)       #leeres Array, damit der erste Punkt nicht dreimal gespeichert wird
    # define steps
    for b in range (0, elements_in_x):                       #keine Anweisung, da für i=0 in der übernächsten Zeile der Punkt ein zweites Mal gespeichert wird
        for i in range(0,elements_in_y):
            for k in range (0,elements_in_z):
                for j in range(0, elements_in_r):
                    next_step = starting_point + (i * step_size_y) + (b * step_size_x) + (j * step_size_r)
                    points_np = np.concatenate((points_np, next_step), axis=0)
    np.savetxt(name_of_csv, points_np, delimiter=",")