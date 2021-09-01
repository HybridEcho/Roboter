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

move.UDP_connection_PXI(parameter.udp_messages.message_PXI_end, parameter.udp_messages.response_PXI_end)
print("End of Experiment")