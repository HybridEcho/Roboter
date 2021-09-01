# ToDo: Tkinter Teil Umwandeln in Obejekt

import tkinter as tk
from mpl_toolkits import mplot3d
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


def set_start_point ():
    xblue = entry_start_point_x_Piezo.get()
    yblue = entry_start_point_y_Piezo.get()
    zblue = entry_start_point_z_Piezo.get()
    rblue = entry_start_point_r_Piezo.get()
    start_position_piezo = np.array([[float(xblue), float(yblue), float(zblue), float(rblue)]])
    np.savetxt("start_position_piezo.csv", start_position_piezo, delimiter=",")

    xred= entry_start_point_x_cMUT.get()
    yred= entry_start_point_y_cMUT.get()
    zred= entry_start_point_z_cMUT.get()
    rred = entry_start_point_r_cMUT.get()
    start_position_cMUT = np.array([[float(xred), float(yred), float(zred), float(rblue)]])
    np.savetxt("start_position_cMUT.csv", start_position_cMUT, delimiter=",")

    depth= entry_depth_over_floor.get()
    text_file = open("depth_over_floor.txt", "w")
    n = text_file.write(str(depth))
    text_file.close()


standard= tk.Tk()
#general Window settings
canvas_start_points = tk.Canvas(standard, width = 600, height = 600)
canvas_start_points.pack()

label_cMUT = tk.Label(standard, text='cMUT')
label_cMUT.config(font=('helvetica', 14))
canvas_start_points.create_window(200, 50, window=label_cMUT)
label_Piezo = tk.Label(standard, text='Piezo')
label_Piezo.config(font=('helvetica', 14))
canvas_start_points.create_window(400, 50, window=label_Piezo)

## x
#cMUT
#settings of entry
entry_start_point_x_cMUT = tk.Entry (standard)
canvas_start_points.create_window(200, 150, window=entry_start_point_x_cMUT)
#naming of entry
label_x_cMUT = tk.Label(standard, text='x:')
label_x_cMUT.config(font=('helvetica', 14))
canvas_start_points.create_window(200, 100, window=label_x_cMUT)
#Piezo
#settings of entry
entry_start_point_x_Piezo = tk.Entry (standard)
canvas_start_points.create_window(400, 150, window=entry_start_point_x_Piezo)
#naming of entry
label_x_Piezo = tk.Label(standard, text='x:')
label_x_Piezo.config(font=('helvetica', 14))
canvas_start_points.create_window(400, 100, window=label_x_Piezo)

## y
#cMUT
#settings of entry
entry_start_point_y_cMUT = tk.Entry (standard)
canvas_start_points.create_window(200, 250, window=entry_start_point_y_cMUT)
#naming of entry
label_y_cMUT = tk.Label(standard, text='y:')
label_y_cMUT.config(font=('helvetica', 16))
canvas_start_points.create_window(200, 200, window=label_y_cMUT)
#Piezo
#settings of entry
entry_start_point_y_Piezo = tk.Entry (standard)
canvas_start_points.create_window(400, 250, window=entry_start_point_y_Piezo)
#naming of entry
label_y_Piezo = tk.Label(standard, text='y:')
label_y_Piezo.config(font=('helvetica', 14))
canvas_start_points.create_window(400, 200, window=label_y_Piezo)

## z
#cMUT
#settings of entry
entry_start_point_z_cMUT = tk.Entry (standard)
canvas_start_points.create_window(200, 350, window=entry_start_point_z_cMUT)
#naming of entry
label_z_cMUT = tk.Label(standard, text='z:')
label_z_cMUT.config(font=('helvetica', 14))
canvas_start_points.create_window(200, 300, window=label_z_cMUT)
#Piezo
#settings of entry
entry_start_point_z_Piezo = tk.Entry (standard)
canvas_start_points.create_window(400, 350, window=entry_start_point_z_Piezo)
#naming of entry
label_z_Piezo = tk.Label(standard, text='z:')
label_z_Piezo.config(font=('helvetica', 14))
canvas_start_points.create_window(400, 300, window=label_z_Piezo)

## r
#cMUT
#settings of entry
entry_start_point_r_cMUT = tk.Entry (standard)
canvas_start_points.create_window(200, 450, window=entry_start_point_r_cMUT)
#naming of entry
label_r_cMUT = tk.Label(standard, text='r:')
label_r_cMUT.config(font=('helvetica', 14))
canvas_start_points.create_window(200, 400, window=label_r_cMUT)
#Piezo
#settings of entry
entry_start_point_r_Piezo = tk.Entry (standard)
canvas_start_points.create_window(400, 450, window=entry_start_point_r_Piezo)
#naming of entry
label_r_Piezo = tk.Label(standard, text='r:')
label_r_Piezo.config(font=('helvetica', 14))
canvas_start_points.create_window(400, 400, window=label_r_Piezo)

#settings of depth
entry_depth_over_floor = tk.Entry (standard)
canvas_start_points.create_window(300, 550, window=entry_depth_over_floor)
#naming of entry
label_depth_over_floor = tk.Label(standard, text='depth over floor:')
label_depth_over_floor.config(font=('helvetica', 14))
canvas_start_points.create_window(300, 500, window=label_depth_over_floor)


button1 = tk.Button(text='set startpoints', command= set_start_point)
canvas_start_points.create_window(300, 400, window=button1)

standard.mainloop()