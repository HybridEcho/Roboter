import tkinter as tk
from mpl_toolkits import mplot3d
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


def set_start_point ():
    xvorne = entry_start_point_x_Piezo.get()
    yvorne = entry_start_point_y_Piezo.get()
    zvorne = entry_start_point_z_Piezo.get()
    start_position_piezo = np.array([[float(xvorne), float(yvorne), float(zvorne)]])
    np.savetxt(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\start_position_piezo.csv", start_position_piezo, delimiter=",")

    xhinten= entry_start_point_x_cMUT.get()
    yhinten= entry_start_point_y_cMUT.get()
    zhinten= entry_start_point_z_cMUT.get()
    start_position_cMUT = np.array([[float(xhinten), float(yhinten), float(zhinten)]])
    np.savetxt(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\start_position_cMUT.csv", start_position_cMUT, delimiter=",")

    depth= entry_depth_over_floor.get()
    text_file = open(r"C:\Users\5GLab\Desktop\Programme\Standard\Testarea\depth_over_floor.txt", "w")
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

#settings of depth
entry_depth_over_floor = tk.Entry (standard)
canvas_start_points.create_window(300, 500, window=entry_depth_over_floor)
#naming of entry
label_depth_over_floor = tk.Label(standard, text='z:')
label_depth_over_floor.config(font=('helvetica', 14))
canvas_start_points.create_window(300, 450, window=label_depth_over_floor)


button1 = tk.Button(text='set startpoints', command= set_start_point)
canvas_start_points.create_window(300, 400, window=button1)

standard.mainloop()




# calculator= tk.Tk()

# canvas1 = tk.Canvas(calculator, width = 400, height = 300)
# canvas1.pack()
# entry1 = tk.Entry (calculator) 
# canvas1.create_window(200, 140, window=entry1)

# def getSquareRoot ():  
#     x1 = entry1.get()
    
#     label1 = tk.Label(calculator, text= float(x1)**0.5)
#     canvas1.create_window(200, 230, window=label1)

#     cMUT_Points = genfromtxt ('cMUT_Points.csv', delimiter=',')
#     Piezo_Points = genfromtxt ('Piezo_Points.csv', delimiter=',')

#     print(cMUT_Points)
#     print(Piezo_Points)

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#     ax.plot(cMUT_Points[:,0], cMUT_Points[:,1], cMUT_Points[:,2],markerfacecolor='r', markeredgecolor='r', marker='o', markersize=5, alpha=0.6)
#     ax.plot(Piezo_Points[:,0], Piezo_Points[:,1], Piezo_Points[:,2],  markerfacecolor='b', markeredgecolor='b', marker='o', markersize=5, alpha=0.6)
#     plt.show()

    
# button1 = tk.Button(text='Get the Square Root', command=getSquareRoot)
# canvas1.create_window(200, 180, window=button1)

# calculator.mainloop()


