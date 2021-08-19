from os import read
import tkinter as tk
import numpy as np
from mpl_toolkits import mplot3d
from numpy import genfromtxt
import matplotlib.pyplot as plt
import math

OptionList_cMUT = [
"number",
"size",
] 
OptionList_Piezo = [
"number",
"size",
] 

depth_over_floor = np.loadtxt("depth_over_floor.txt", dtype=float)

def calculat ():
    condition=variable_Piezo.get()
    #### cMUT System ####
    # get values
    global x_pitch_cMUT, y_pitch_cMUT, number_cMUT_in_x, number_cMUT_in_y, x_pitch_Piezo, y_pitch_Piezo, number_Piezo_in_x, number_Piezo_in_y, cMUT_Points, Piezo_Points, entry_size_of_cMUT_in_x, entry_size_of_cMUT_in_y, entry_size_of_Piezo_in_x, size_of_Piezo_in_y
    
    x_pitch_cMUT = entry_x_pitch_cMUT.get()
    x_pitch_cMUT = float(x_pitch_cMUT)
    y_pitch_cMUT = entry_y_pitch_cMUT.get()
    y_pitch_cMUT = float(y_pitch_cMUT)

    if  condition == "size":
        size_of_cMUT_in_x = float(entry_size_of_cMUT_in_x.get())
        size_of_cMUT_in_y = float(entry_size_of_cMUT_in_y.get())
        number_cMUT_in_x = size_of_cMUT_in_x/x_pitch_cMUT
        number_cMUT_in_y = size_of_cMUT_in_y/y_pitch_cMUT
        number_cMUT_in_x = int(number_cMUT_in_x)
        number_cMUT_in_y = int(number_cMUT_in_y)
   
    elif condition == "number":
        number_cMUT_in_x = entry_number_cMUT_in_x.get()
        number_cMUT_in_x = int(number_cMUT_in_x)
        number_cMUT_in_y = entry_number_cMUT_in_y.get()
        number_cMUT_in_y = int(number_cMUT_in_y)

    # define startposition and stepsize
    start_cMUT = genfromtxt ("start_position_cMUT.csv", delimiter=',')
    step_size_y_cMUT = np.array([[0, y_pitch_cMUT, 0]])
    step_size_x_cMUT = np.array([[x_pitch_cMUT, 0, 0]])

    #cMUT_Points = start_cMUT
    cMUT_Points = np.array([[]]).reshape(0,3)       #leeres Array, damit der erste Punkt nicht dreimal gespeichert wird
    # define steps
    for b in range (0, number_cMUT_in_x):                       #keine Anweisung, da für i=0 in der übernächsten Zeile der Punkt ein zweites Mal gespeichert wird
        for i in range(0,number_cMUT_in_y):
            next_step_xy_cMUT = start_cMUT - (i * step_size_y_cMUT) - (b * step_size_x_cMUT)
            cMUT_Points = np.concatenate((cMUT_Points, next_step_xy_cMUT), axis=0)

    #np.savetxt(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\cMUT_Points_std_coord.csv", cMUT_Points_std_coord, delimiter=",")
    np.savetxt("cMUT_Points.csv", cMUT_Points, delimiter=",")
    cMUT_Points_std = cMUT_Points
    cMUT_Points_std [:, 2]=depth_over_floor
    np.savetxt("cMUT_Points_std.csv", cMUT_Points_std, delimiter=",")

    

    #### Piezo-System ####

    # get values
    x_pitch_Piezo = float(entry_x_pitch_Piezo.get())
    y_pitch_Piezo = float(entry_y_pitch_Piezo.get())

    if  condition == "size":
        size_of_Piezo_in_x = float(entry_size_of_Piezo_in_x.get())
        size_of_Piezo_in_y = float(entry_size_of_Piezo_in_y.get())
        number_Piezo_in_x = size_of_Piezo_in_x/x_pitch_Piezo
        number_Piezo_in_y = size_of_Piezo_in_y/y_pitch_Piezo
        number_Piezo_in_x = int(number_Piezo_in_x)
        number_Piezo_in_y = int(number_Piezo_in_y) 

    elif condition == "number":
        number_Piezo_in_x = int(entry_number_Piezo_in_x.get())
        number_Piezo_in_y = int(entry_number_Piezo_in_y.get())
   
    else:
        print("error")

    # define startposition and stepsize
    start_Piezo = genfromtxt ("start_position_piezo.csv", delimiter=',')
    step_size_y_Piezo = np.array([[0, y_pitch_Piezo, 0]])
    step_size_x_Piezo = np.array([[x_pitch_Piezo, 0, 0]])
    Piezo_Points = np.array([[]]).reshape(0,3)

    # define steps
    for b in range(0,number_Piezo_in_x):
        for i in range(0,number_Piezo_in_y):
           next_step_y_Piezo = start_Piezo + (i * step_size_y_Piezo) + (b * step_size_x_Piezo)
           Piezo_Points = np.concatenate((Piezo_Points, next_step_y_Piezo), axis=0)

    np.savetxt("Piezo_Points.csv", Piezo_Points, delimiter=",")

    # standardisieren der Piezo Punkte
    Piezo_Points_std = Piezo_Points
    Piezo_Points_std [:, 2]=depth_over_floor
    Piezo_Points_std=([685 , -200, 0] - Piezo_Points_std) * [1, 1, -1]

    np.savetxt("Piezo_Points_std.csv", Piezo_Points_std, delimiter=",")

def condition_Piezo ():
    condition=variable_Piezo.get()
    global entry_size_of_Piezo_in_x, entry_size_of_Piezo_in_y

    if  condition == "size":
        #settings of Piezo size in x
        entry_size_of_Piezo_in_x = tk.Entry (calculator)
        canvas_calculator.create_window(400, 350, window=entry_size_of_Piezo_in_x)
        #naming of piezo size
        size_of_Piezo_in_x = tk.Label(calculator, text='size in x:')
        size_of_Piezo_in_x.config(font=('helvetica', 14))
        size_of_Piezo_in_x.config(width=10)
        canvas_calculator.create_window(400, 310, window=size_of_Piezo_in_x)

        #settings of Piezo size in y
        entry_size_of_Piezo_in_y = tk.Entry (calculator)
        canvas_calculator.create_window(400, 450, window=entry_size_of_Piezo_in_y)
        #naming of piezo size
        size_of_Piezo_in_y = tk.Label(calculator, text='size in y:')
        size_of_Piezo_in_y.config(font=('helvetica', 14))
        size_of_Piezo_in_y.config(width=10)
        canvas_calculator.create_window(400, 410, window=size_of_Piezo_in_y)

    elif condition == "number":
        #naming of piezo number
        number_Piezo_in_x = tk.Label(calculator, text='number in x')
        number_Piezo_in_x.config(font=('helvetica', 14))
        canvas_calculator.create_window(400, 310, window=number_Piezo_in_x)
        #naming of piezo number
        number_Piezo_in_y = tk.Label(calculator, text='number in y')
        number_Piezo_in_y.config(font=('helvetica', 14))
        canvas_calculator.create_window(400, 410, window=number_Piezo_in_y)

    else:
        #naming to chose
        hinweis1 = tk.Label(calculator, text='number c in y')
        hinweis1.config(font=('helvetica', 14))
        canvas_calculator.create_window(200, 450, window=hinweis1)

def condition_cMUT ():
    condition=variable_cMUT.get()
    global entry_size_of_cMUT_in_x, entry_size_of_cMUT_in_y

    if  condition == "size":
        #settings of cMUT size in x
        entry_size_of_cMUT_in_x = tk.Entry (calculator)
        canvas_calculator.create_window(200, 350, window=entry_size_of_cMUT_in_x)
        #naming of cMUT size
        size_of_cMUT_in_x = tk.Label(calculator, text='size in x:')
        size_of_cMUT_in_x.config(font=('helvetica', 14))
        size_of_cMUT_in_x.config(width=10)
        canvas_calculator.create_window(200, 310, window=size_of_cMUT_in_x)

        #settings of cMUT size in y
        entry_size_of_cMUT_in_y = tk.Entry (calculator)
        canvas_calculator.create_window(200, 450, window=entry_size_of_cMUT_in_y)
        #naming of cMUT size
        size_of_cMUT_in_y = tk.Label(calculator, text='size x')
        size_of_cMUT_in_y.config(font=('helvetica', 14))
        size_of_cMUT_in_y.config(width=10)
        canvas_calculator.create_window(200, 410, window=size_of_cMUT_in_y)

    elif condition == "number":
        #naming of cMUT number
        number_cMUT_in_x = tk.Label(calculator, text='number in x')
        number_cMUT_in_x.config(font=('helvetica', 14))
        canvas_calculator.create_window(200, 310, window=number_cMUT_in_x)
        #naming of cMUT number
        number_cMUT_in_y = tk.Label(calculator, text='number in y')
        number_cMUT_in_y.config(font=('helvetica', 14))
        canvas_calculator.create_window(200, 410, window=number_cMUT_in_y)

    else:
        #naming to chose
        hinweis1 = tk.Label(calculator, text='Error')
        hinweis1.config(font=('helvetica', 14))
        canvas_calculator.create_window(200, 450, window=hinweis1)

def point_plot ():
    cMUT_Points_std = genfromtxt ('cMUT_Points_std.csv', delimiter=',')
    Piezo_Points_std = genfromtxt ('Piezo_Points_std.csv', delimiter=',')

    cMUT_Points_std = np.array(cMUT_Points_std, ndmin=2)
    Piezo_Points_std = np.array(Piezo_Points_std, ndmin=2)

    print("Standard cMUT Points")
    print(cMUT_Points_std)
    print("")
    print("Standard Piezo Points")
    print(Piezo_Points_std)
    print("")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(cMUT_Points_std[:,0], cMUT_Points_std[:,1], cMUT_Points_std[:,2],markerfacecolor='r', markeredgecolor='r', marker='o', markersize=5, alpha=0.6)
    ax.plot(Piezo_Points_std[:,0], Piezo_Points_std[:,1], Piezo_Points_std[:,2],  markerfacecolor='b', markeredgecolor='b', marker='o', markersize=5, alpha=0.6)
    plt.show()

def duration ():
    measurementtime=(len(cMUT_Points)*len(Piezo_Points))*3/60
    #naming of duration
    label_duration = tk.Label(calculator, text= "Estimated time: " + str(measurementtime) + " min.")
    label_duration.config(font=('helvetica', 14))
    canvas_calculator.create_window(300, 550, window=label_duration)



calculator= tk.Tk()
#general Window settings
canvas_calculator = tk.Canvas(calculator, width = 600, height = 600)
canvas_calculator.pack()

label_cMUT = tk.Label(calculator, text='cMUT')
label_cMUT.config(font=('helvetica', 14))
canvas_calculator.create_window(200, 50, window=label_cMUT)
label_Piezo = tk.Label(calculator, text='Piezo')
label_Piezo.config(font=('helvetica', 14))
canvas_calculator.create_window(400, 50, window=label_Piezo)

#cMUT
#settings of x pitch
entry_x_pitch_cMUT = tk.Entry (calculator)
canvas_calculator.create_window(200, 150, window=entry_x_pitch_cMUT)
#naming of entry
label_x_pitch_cMUT = tk.Label(calculator, text='pitch x:')
label_x_pitch_cMUT.config(font=('helvetica', 14))
canvas_calculator.create_window(200, 100, window=label_x_pitch_cMUT)

#Piezo
#settings of x pitch
entry_x_pitch_Piezo = tk.Entry (calculator)
canvas_calculator.create_window(400, 150, window=entry_x_pitch_Piezo)
#naming of entry
label_x_pitch_Piezo = tk.Label(calculator, text='pitch x:')
label_x_pitch_Piezo.config(font=('helvetica', 14))
canvas_calculator.create_window(400, 100, window=label_x_pitch_Piezo)

#cMUT
#settings of y pitch
entry_y_pitch_cMUT = tk.Entry (calculator)
canvas_calculator.create_window(200, 250, window=entry_y_pitch_cMUT)
#naming of entry
label_y_pitch_cMUT = tk.Label(calculator, text='pitch y:')
label_y_pitch_cMUT.config(font=('helvetica', 16))
canvas_calculator.create_window(200, 200, window=label_y_pitch_cMUT)

#Piezo
#settings of y pitch
entry_y_pitch_Piezo = tk.Entry (calculator)
canvas_calculator.create_window(400, 250, window=entry_y_pitch_Piezo)
#naming of enty_pitchy
label_y_pitch_Piezo = tk.Label(calculator, text='pitch y:')
label_y_pitch_Piezo.config(font=('helvetica', 14))
canvas_calculator.create_window(400, 200, window=label_y_pitch_Piezo)

#settings of Piezo number in x
entry_number_Piezo_in_x = tk.Entry (calculator)
canvas_calculator.create_window(400, 350, window=entry_number_Piezo_in_x)
#settings of Piezo number in y
entry_number_Piezo_in_y = tk.Entry (calculator)
canvas_calculator.create_window(400, 450, window=entry_number_Piezo_in_y)
#settings of cMUT number in x
entry_number_cMUT_in_x = tk.Entry (calculator)
canvas_calculator.create_window(200, 350, window=entry_number_cMUT_in_x)
#settings of cMUT number in y
entry_number_cMUT_in_y = tk.Entry (calculator)
canvas_calculator.create_window(200, 450, window=entry_number_cMUT_in_y)

#drop down
variable_cMUT = tk.StringVar(calculator)
variable_cMUT.set(OptionList_cMUT[0])
opt_cMUT = tk.OptionMenu(calculator, variable_cMUT, *OptionList_cMUT)
opt_cMUT.config(width=10)
canvas_calculator.create_window(200, 280, window=opt_cMUT)

variable_Piezo = tk.StringVar(calculator)
variable_Piezo.set(OptionList_Piezo[0])
opt_Piezo = tk.OptionMenu(calculator, variable_Piezo, *OptionList_Piezo)
opt_Piezo.config(width=10)
canvas_calculator.create_window(400, 280, window=opt_Piezo)

condition_cMUT ()
condition_Piezo ()

button1 = tk.Button(text='update', command= lambda:[condition_Piezo(), condition_cMUT()] )
canvas_calculator.create_window(300, 280, window=button1)

button2 = tk.Button(text='calculat points', command= lambda:[calculat(), duration()])
canvas_calculator.create_window(300, 500, window=button2)

button3 = tk.Button(text='plot points', command= point_plot)
canvas_calculator.create_window(300, 450, window=button3)

calculator.mainloop()