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

def line_up_points_from_csv():
    cMUT = np.array([[parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,0], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,1], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,2], parameter.import_csv.load_cMUT_points_np()[number_of_cmut_measurement,3]]])
    Piezo = np.array([[parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,0], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,1], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,2], parameter.import_csv.load_piezo_points_np()[number_of_piezo_measurement,3]]])
    combined= np.concatenate((Piezo, cMUT), axis=1)
    combined_csv= np.concatenate((combined_csv, combined), axis=0)
    


def line_by_line_combining():
    combined_csv=np.array([[]]).reshape(0,8)
    for number_of_piezo_measurement in range((len(parameter.import_csv.load_piezo_points_np()))):
        number_of_cmut_measurement = number_of_piezo_measurement
        line_up_points_from_csv()
        
    np.savetxt("Combined_Points.csv", combined_csv, delimiter=",")
