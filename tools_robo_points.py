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

def adding_a_line_to_combined_np(number_of_cmut_measurement, number_of_piezo_measurement, combined_np):
    cMUT = np.array([[parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,0], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,1], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,2], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,3]]])
    Piezo = np.array([[parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,0], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,1], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,2], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,3]]])
    combined= np.concatenate((Piezo, cMUT), axis=1)
    combined_np= np.concatenate((combined_np, combined), axis=0)
    return combined_np

def combining_line_by_line():
    combined_np=np.array([[]]).reshape(0,8)
    for number_of_piezo_measurement in range((len(parameter.import_csv.load_piezo_points_np()))):
        number_of_cmut_measurement = number_of_piezo_measurement
        combined_np = adding_a_line_to_combined_np(number_of_cmut_measurement, number_of_piezo_measurement, combined_np)
    np.savetxt("Combined_Points.csv", combined_np, delimiter=",")
    print(combined_np)

# def combining_all():
#     combined_np=np.array([[]]).reshape(0,8)
#     for number_of_piezo_measurement in range((len(parameter.import_csv.load_piezo_points_np()))):
#         for number_of_cmut_measurement in range((len(parameter.import_csv.load_cMUT_points_np()))):
#             adding_a_line_to_combined_np(number_of_cmut_measurement, number_of_piezo_measurement, combined_np)

#     np.savetxt("Combined_Points.csv", combined_np, delimiter=",")


# def condition_transform():
#      if  condition == "size":
#          size_of_cMUT_in_x = float(entry_size_of_cMUT_in_x.get())
#         size_of_cMUT_in_y = float(entry_size_of_cMUT_in_y.get())
#         number_cMUT_in_x = size_of_cMUT_in_x/x_pitch_cMUT
#         number_cMUT_in_y = size_of_cMUT_in_y/y_pitch_cMUT
#         number_cMUT_in_x = int(number_cMUT_in_x)
#         number_cMUT_in_y = int(number_cMUT_in_y)

#     elif condition == "number":
#         number_cMUT_in_x = entry_number_cMUT_in_x.get()
#         number_cMUT_in_x = int(number_cMUT_in_x)
#         number_cMUT_in_y = entry_number_cMUT_in_y.get()
#         number_cMUT_in_y = int(number_cMUT_in_y)

def calculat_csv(entry_x_pitch_cMUT.get(), number_cMUT_in_x.get(), entry_y_pitch_cMUT.get(), number_cMUT_in_y.get(), genfromtxt ("start_position_cMUT.csv", delimiter=','))

def calculat_np(x_pitch, elements_in_x, y_pitch, elements_in_y, r_pitch, elements_in_r, starting_point):
    x_pitch = float(x_pitch)
    y_pitch = float(y_pitch)
    r_pitch = float(r_pitch)
    # define startposition and stepsize
    step_size_y = np.array([[0, y_pitch, 0, 0]])
    step_size_x = np.array([[x_pitch, 0, 0, 0]])
    step_size_r = np.array([[0, 0, 0, r_pitch]])

    #cMUT_Points = start_cMUT
    points_np = np.array([[]]).reshape(0,4)       #leeres Array, damit der erste Punkt nicht dreimal gespeichert wird
    # define steps
    for b in range (0, elements_in_x):                       #keine Anweisung, da für i=0 in der übernächsten Zeile der Punkt ein zweites Mal gespeichert wird
        for i in range(0,elements_in_y):
            for j in range(0, elements_in_r:)
            next_step = starting_point + (i * step_size_y) + (b * step_size_x) + (j * step_size_r)
            points_np = np.concatenate((Points_np, next_step), axis=0)

    return points_np
    #np.savetxt(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\cMUT_Points_std_coord.csv", cMUT_Points_std_coord, delimiter=",")

def save_np_as_csv (np_array, string_name_of_csv):
    name_of_csv = string_name_of_csv + ".csv"
    np.savetxt(name_of_csv, np_array, delimiter=",")
    cMUT_Points_std = cMUT_Points
    cMUT_Points_std [:, 2]=depth_over_floor
    np.savetxt("cMUT_Points_std.csv", cMUT_Points_std, delimiter=",")



# def calculat ():
#     condition=variable_Piezo.get()
    
#     #### cMUT System ####
#     # get values
#     global x_pitch_cMUT, y_pitch_cMUT, number_cMUT_in_x, number_cMUT_in_y, x_pitch_Piezo, y_pitch_Piezo, number_Piezo_in_x, number_Piezo_in_y, cMUT_Points, Piezo_Points, entry_size_of_cMUT_in_x, entry_size_of_cMUT_in_y, entry_size_of_Piezo_in_x, size_of_Piezo_in_y

#     x_pitch_cMUT = entry_x_pitch_cMUT.get()
#     x_pitch_cMUT = float(x_pitch_cMUT)
#     y_pitch_cMUT = entry_y_pitch_cMUT.get()
#     y_pitch_cMUT = float(y_pitch_cMUT)

#     if  condition == "size":
#         size_of_cMUT_in_x = float(entry_size_of_cMUT_in_x.get())
#         size_of_cMUT_in_y = float(entry_size_of_cMUT_in_y.get())
#         number_cMUT_in_x = size_of_cMUT_in_x/x_pitch_cMUT
#         number_cMUT_in_y = size_of_cMUT_in_y/y_pitch_cMUT
#         number_cMUT_in_x = int(number_cMUT_in_x)
#         number_cMUT_in_y = int(number_cMUT_in_y)

#     elif condition == "number":
#         number_cMUT_in_x = entry_number_cMUT_in_x.get()
#         number_cMUT_in_x = int(number_cMUT_in_x)
#         number_cMUT_in_y = entry_number_cMUT_in_y.get()
#         number_cMUT_in_y = int(number_cMUT_in_y)

#     # define startposition and stepsize
#     start_cMUT = genfromtxt ("start_position_cMUT.csv", delimiter=',')
#     step_size_y_cMUT = np.array([[0, y_pitch_cMUT, 0, 0]])
#     step_size_x_cMUT = np.array([[x_pitch_cMUT, 0, 0, 0]])

#     #cMUT_Points = start_cMUT
#     cMUT_Points = np.array([[]]).reshape(0,4)       #leeres Array, damit der erste Punkt nicht dreimal gespeichert wird
#     # define steps
#     for b in range (0, number_cMUT_in_x):                       #keine Anweisung, da für i=0 in der übernächsten Zeile der Punkt ein zweites Mal gespeichert wird
#         for i in range(0,number_cMUT_in_y):
#             next_step_xy_cMUT = start_cMUT - (i * step_size_y_cMUT) - (b * step_size_x_cMUT)
#             cMUT_Points = np.concatenate((cMUT_Points, next_step_xy_cMUT), axis=0)

#     #np.savetxt(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\cMUT_Points_std_coord.csv", cMUT_Points_std_coord, delimiter=",")
#     np.savetxt("cMUT_Points.csv", cMUT_Points, delimiter=",")
#     cMUT_Points_std = cMUT_Points
#     cMUT_Points_std [:, 2]=depth_over_floor
#     np.savetxt("cMUT_Points_std.csv", cMUT_Points_std, delimiter=",")



#     #### Piezo-System ####

#     # get values
#     x_pitch_Piezo = float(entry_x_pitch_Piezo.get())
#     y_pitch_Piezo = float(entry_y_pitch_Piezo.get())

#     if  condition == "size":
#         size_of_Piezo_in_x = float(entry_size_of_Piezo_in_x.get())
#         size_of_Piezo_in_y = float(entry_size_of_Piezo_in_y.get())
#         number_Piezo_in_x = size_of_Piezo_in_x/x_pitch_Piezo
#         number_Piezo_in_y = size_of_Piezo_in_y/y_pitch_Piezo
#         number_Piezo_in_x = int(number_Piezo_in_x)
#         number_Piezo_in_y = int(number_Piezo_in_y) 

#     elif condition == "number":
#         number_Piezo_in_x = int(entry_number_Piezo_in_x.get())
#         number_Piezo_in_y = int(entry_number_Piezo_in_y.get())

#     else:
#         print("error")

#     # define startposition and stepsize
#     start_Piezo = genfromtxt ("start_position_piezo.csv", delimiter=',')
#     step_size_y_Piezo = np.array([[0, y_pitch_Piezo, 0, 0]])
#     step_size_x_Piezo = np.array([[x_pitch_Piezo, 0, 0, 0]])
#     Piezo_Points = np.array([[]]).reshape(0,4)

#     # define steps
#     for b in range(0,number_Piezo_in_x):
#         for i in range(0,number_Piezo_in_y):
#             next_step_y_Piezo = start_Piezo + (i * step_size_y_Piezo) + (b * step_size_x_Piezo)
#             Piezo_Points = np.concatenate((Piezo_Points, next_step_y_Piezo), axis=0)

#     np.savetxt("Piezo_Points.csv", Piezo_Points, delimiter=",")

#     # standardisieren der Piezo Punkte
#     Piezo_Points_std = Piezo_Points
#     Piezo_Points_std [:, 2]=depth_over_floor
#     Piezo_Points_std=([685 , -200, 0, 0] - Piezo_Points_std) * [1, 1, -1, -1]

#     np.savetxt("Piezo_Points_std.csv", Piezo_Points_std, delimiter=",")