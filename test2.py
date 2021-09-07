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

class input_variables:
    def getting_value(value):
        value=float(value.get())
        return value