import os
import tkinter as tk
import numpy as np
from mpl_toolkits import mplot3d
from numpy import genfromtxt
import matplotlib.pyplot as plt
import math
import parameter
import tools_robo_points
import pickle

depth_over_floor = np.loadtxt("depth_over_floor.txt", dtype=float)

######################## functions for GUI buttons################

def calculat ():
    values_robo_blue, values_robo_red=get_values()
    print(values_robo_blue)
    print(values_robo_red)
    tools_robo_points.calculat_np("blue_Points", **values_robo_blue)
    tools_robo_points.calculat_np("red_Points", **values_robo_red )

def combining_line_by_line():
    tools_robo_points.combining_line_by_line()

def combining_all():
    tools_robo_points.combining_all()

def point_plot ():
    red_Points_std = genfromtxt ('red_Points_std.csv', delimiter=',')
    blue_Points_std = genfromtxt ('blue_Points_std.csv', delimiter=',')

    red_Points_std = np.array(red_Points_std, ndmin=2)
    blue_Points_std = np.array(blue_Points_std, ndmin=2)

    print("Standard red Points")
    print(red_Points_std)
    print("")
    print("Standard blue Points")
    print(blue_Points_std)
    print("")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(red_Points_std[:,0], red_Points_std[:,1], red_Points_std[:,2],markerfacecolor='r', markeredgecolor='r', marker='o', markersize=5, alpha=0.6)
    ax.plot(blue_Points_std[:,0], blue_Points_std[:,1], blue_Points_std[:,2],  markerfacecolor='b', markeredgecolor='b', marker='o', markersize=5, alpha=0.6)
    plt.show()

def duration ():
    print("Finaly")
    measurementtime=(len(np.genfromtxt ("combined_points.csv", delimiter=',')))*3/60
    print(measurementtime)
    # #naming of duration
    # label_duration = tk.Label(calculator, text= "Estimated time: " + str(measurementtime) + " min.")
    # label_duration.config(font=('helvetica', 14))
    # canvas_calculator.create_window(300, 550, window=label_duration)

########################## GUI set-up functions and Parameters ####################

def naming_gui_fields(entry, label, x_position, y_position):
    canvas_calculator.create_window(x_position+50, y_position+50, window=entry)
    #naming of entry
    text_label=label.replace("_", " ").replace("label", "")
    text_label=text_label.replace("red", "").replace("blue","")
    print(text_label)
    label = tk.Label(calculator, text= text_label)
    label.config(font=('helvetica', 14))
    canvas_calculator.create_window(x_position, y_position, window=label)

def get_values():
    values_robo_blue={
        "starting_point": genfromtxt ("start_position_blue.csv", delimiter=','),
        "x_pitch":float(entry_x_pitch_blue.get()) , "elements_in_x":int(entry_number_blue_in_x.get()), 
        "y_pitch":float(entry_y_pitch_blue.get()), "elements_in_y":int(entry_number_blue_in_y.get()),
        "z_pitch":float(entry_z_pitch_blue.get()), "elements_in_z":int(entry_number_blue_in_z.get()), 
        "r_pitch":float(entry_r_pitch_blue.get()), "elements_in_r":int(entry_number_blue_in_r.get())}
    with open('values_robo_blue.txt','wb') as datafile: 
        pickle.dump(values_robo_blue, datafile)
    values_robo_red={
        "starting_point": genfromtxt ("start_position_red.csv", delimiter=','),
        "x_pitch":float(entry_x_pitch_red.get()), "elements_in_x":int(entry_number_red_in_x.get()), 
        "y_pitch":float(entry_y_pitch_red.get()), "elements_in_y":int(entry_number_red_in_y.get()),
        "z_pitch":float(entry_z_pitch_red.get()), "elements_in_z":int(entry_number_red_in_z.get()),  
        "r_pitch":float(entry_r_pitch_red.get()), "elements_in_r":int(entry_number_red_in_r.get())}
    with open('values_robo_red.txt','wb') as datafile: 
        pickle.dump(values_robo_red, datafile)
    return values_robo_blue, values_robo_red

old_values_robo_blue = parameter.import_text.load_text("values_robo_blue")
old_values_robo_red = parameter.import_text.load_text("values_robo_red")

######################## general GUI Window settings ##################
calculator= tk.Tk()
canvas_calculator = tk.Canvas(calculator, width = 1500, height =700)
canvas_calculator.pack()
label_red = tk.Label(calculator, text='Red Robot')
label_red.config(font=('helvetica', 14))
canvas_calculator.create_window(200, 50, window=label_red)
label_blue = tk.Label(calculator, text='Blue Robot')
label_blue.config(font=('helvetica', 14))
canvas_calculator.create_window(400, 50, window=label_blue)

############################# Entry Fields in GUI ################

entry_x_pitch_red = tk.Entry (calculator)
entry_x_pitch_red.insert(0, old_values_robo_red["x_pitch"])
naming_gui_fields(entry_x_pitch_red,'label_x_pitch_red', 100, 100)
entry_x_pitch_blue = tk.Entry (calculator)
entry_x_pitch_blue.insert(0, old_values_robo_blue["x_pitch"])
naming_gui_fields(entry_x_pitch_blue, 'label_x_pitch_blue', 300, 100)
entry_y_pitch_red= tk.Entry (calculator)
entry_y_pitch_red.insert(0, old_values_robo_red["y_pitch"])
naming_gui_fields(entry_y_pitch_red, "label_y_pitch_red", 100, 200)
entry_y_pitch_blue= tk.Entry (calculator)
entry_y_pitch_blue.insert(0, old_values_robo_blue["y_pitch"])
naming_gui_fields(entry_y_pitch_blue, "label_y_pitch_blue", 300, 200)
entry_z_pitch_red= tk.Entry (calculator)
entry_z_pitch_red.insert(0, old_values_robo_red["z_pitch"])
naming_gui_fields(entry_z_pitch_red, "label_z_pitch_red", 100, 300)
entry_z_pitch_blue = tk.Entry (calculator)
entry_z_pitch_blue.insert(0, old_values_robo_blue["z_pitch"])
naming_gui_fields(entry_z_pitch_blue, "label_z_pitch_blue", 300, 300)
entry_r_pitch_red = tk.Entry (calculator)
entry_r_pitch_red.insert(0, old_values_robo_red["r_pitch"])
naming_gui_fields(entry_r_pitch_red, "label_r_pitch_red", 100, 400)
entry_r_pitch_blue = tk.Entry (calculator)
entry_r_pitch_blue.insert(0, old_values_robo_blue["r_pitch"])
naming_gui_fields(entry_r_pitch_blue, "label_r_pitch_blue", 300, 400)
entry_number_red_in_x = tk.Entry (calculator)
entry_number_red_in_x.insert(0, old_values_robo_red["elements_in_x"])
naming_gui_fields(entry_number_red_in_x, "label_number_red_in_x", 600, 100)
entry_number_blue_in_x = tk.Entry (calculator)
entry_number_blue_in_x.insert(0, old_values_robo_blue["elements_in_x"])
naming_gui_fields(entry_number_blue_in_x, "label_number_blue_in_x", 1000, 100)
entry_number_red_in_y = tk.Entry (calculator)
entry_number_red_in_y.insert(0, old_values_robo_red["elements_in_y"])
naming_gui_fields(entry_number_red_in_y, "label_number_red_in_y", 600, 200)
entry_number_blue_in_y = tk.Entry (calculator)
entry_number_blue_in_y.insert(0, old_values_robo_blue["elements_in_y"])
naming_gui_fields(entry_number_blue_in_y, "label_number_blue_in_y", 1000, 200)
entry_number_red_in_z = tk.Entry (calculator)
entry_number_red_in_z.insert(0, old_values_robo_red["elements_in_z"])
naming_gui_fields(entry_number_red_in_z, "label_number_red_in_z",600, 300)
entry_number_blue_in_z = tk.Entry (calculator)
entry_number_blue_in_z.insert(0, old_values_robo_blue["elements_in_z"])
naming_gui_fields(entry_number_blue_in_z, "label_number_blue_in_z", 1000, 300)
entry_number_red_in_r = tk.Entry (calculator)
entry_number_red_in_r.insert(0, old_values_robo_red["elements_in_r"])
naming_gui_fields(entry_number_red_in_r, "label_number_red_in_r",600, 400)
entry_number_blue_in_r = tk.Entry (calculator)
entry_number_blue_in_r.insert(0, old_values_robo_blue["elements_in_r"])
naming_gui_fields(entry_number_blue_in_r, "label_number_blue_in_r", 1000, 400)

################################## Buttons in GUI ###########
button2 = tk.Button(text='calculat points', command= lambda:[calculat(), duration()])
canvas_calculator.create_window(500, 500, window=button2)

button3 = tk.Button(text='plot points', command= point_plot)
canvas_calculator.create_window(500, 550, window=button3)

button4 = tk.Button(text='combin all', command= combining_all)
canvas_calculator.create_window(500, 600, window=button4)

button5 = tk.Button(text='line by line', command= combining_line_by_line)
canvas_calculator.create_window(500, 650, window=button5)

calculator.mainloop()