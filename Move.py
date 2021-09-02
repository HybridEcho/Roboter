#-ToDo:
#- Bei Feedback Roboname mit senden

from os import read
import telnetlib
import time
from tkinter.constants import SEL_FIRST
import numpy as np
import socket 
import parameter

def UDP_connection_PXI (message, response):
    start_time = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    answer_PXI = ""
    while answer_PXI != response.encode("UTF-8"):
        s.sendto((message.encode("ascii")), (parameter.network_parameters.ip_PXI, parameter.network_parameters.port_PXI))
        try:
            s.settimeout(100)
            daten, addr = s.recvfrom(1024)
            answer_PXI = daten
            nice_output_PXI = daten
            print("    Status PXI: " + str(nice_output_PXI) )
        except:
            print("PXI did not echo to " + message + ", will try again")
        if (time.time() - start_time > 10):
            print("PXI did not echo after 10s of repeated", message, "sending, Programm ende")
            exit()

def roboter_message (tn_robo, message):
    message=message
    tn_robo.write(message)
    print("send Message")
    if message == "MOV\r\n".encode("ascii"):
        tn_robo.read_until("Doesntmatter".encode("ascii"), 0.5)
    else:
        print(" ")

def roboter_feedback(tn_robo, exp_feedback_ascii):
    info_from_robo_ascii = tn_robo.read_until(exp_feedback_ascii, 3.0)
    info_from_robo = info_from_robo_ascii.decode("ascii")
    info_from_robo = str(info_from_robo)
    exp_feedback = exp_feedback_ascii.decode("ascii")
    exp_feedback =str(exp_feedback)
    if exp_feedback not in info_from_robo:
        print("Error-Schleife")
        print(info_from_robo)
        error = tn_robo.read_until("doesntmatter".encode("ascii"), 3.0)
        print(error)
        return(error)
    elif "P" in info_from_robo:
        print("P-Schleife")
        message_from_robo = tn_robo.read_until("\n".encode("ascii"))
        message_from_robo = message_from_robo.decode("ascii")
        message_from_robo = message_from_robo.strip("\n""\r")
        print(message_from_robo)
    elif "WRONG" in info_from_robo:
        print(info_from_robo)
        return(info_from_robo)

def roboter_movement_by_csv(number_of_measurement, csv_data, tn_robo):
    roboter_message(tn_robo, ("MOV\r\n".encode("ascii")))
    print("start Message was send")
    if tn_robo == parameter.network_parameters.tnred :
        message_robo_point_np = np.array([csv_data[number_of_measurement,4], csv_data[number_of_measurement,5], csv_data[number_of_measurement,6], csv_data[number_of_measurement,7]])
        message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
        message_robo_point_string = message_robo_point_prestring.strip('['']')
        print(message_robo_point_string)
    else:
        message_robo_point_np = np.array([csv_data[number_of_measurement,0], csv_data[number_of_measurement,1], csv_data[number_of_measurement,2], csv_data[number_of_measurement,3]])
        message_robo_point_prestring = np.array2string(message_robo_point_np, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
        message_robo_point_string = message_robo_point_prestring.strip('['']')
        print(message_robo_point_string)
    message_robo_point="P1 = ".encode("ascii") + message_robo_point_string.encode("ascii") + " 0 0 1\r\n".encode("ascii")
    roboter_message(tn_robo, message_robo_point)
    print("Point Message was send")
    roboter_feedback(tn_robo, "P11=".encode("ascii"))


########################################################################################################


# for a in range(len(piezo_Points_np)):
#     for b in range(len(cMUT_Points_np)):
#         number_of_measurements=len(cMUT_Points_np)*len(piezo_Points_np)
#         current_measurment= (b+1 + a*len(cMUT_Points_np))
#         print("Measurement " +str(current_measurment) + "of " + str(number_of_measurements))
#         #line by line reading of csv file
#         cMUT = np.array([cMUT_Points_np[b,0], cMUT_Points_np[b,1], cMUT_Points_np[b,2]])
#         Piezo = np.array([piezo_Points_np[a,0], piezo_Points_np[a,1], piezo_Points_np[a,2]])

#         ##transforming the single points to robo-readable format
#         cMUT_prestring = np.array2string(cMUT, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
#         cMUT_string = cMUT_prestring.strip('['']')
#         Piezo_prestring = np.array2string(Piezo, precision=3, separator=' ', floatmode='fixed',  suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
#         Piezo_string = Piezo_prestring.strip('['']')

#         ##generation of the robo-message
#         message_cMUT="P1 = ".encode("ascii") + cMUT_string.encode("ascii") + "0 0 0 1\r\n".encode("ascii")
#         message_Piezo="P1 = ".encode("ascii") + Piezo_string.encode("ascii") + "0 0 0 1\r\n".encode("ascii")

#         ## transfere of point data to Robo
#         tnred.write(message_cMUT)
#         tnblue.write(message_Piezo)

#         ##control via Feedback from Robot
#         act_position_robo_hinten = tnred.expect(["P11=".encode("ascii"), "ERROR".encode("ascii")], 1.0)
#         print(act_position_robo_hinten)
#         if "ERROR".encode("ascii") in act_position_robo_hinten :
#             tnred.read_until("doesntmatter".encode("ascii"), 1.0)
#             exit()
#         else:
#             act_position_robo_hinten = tnred.read_until("\n".encode("ascii"))
#             act_position_robo_hinten = act_position_robo_hinten.decode("ascii")
#             act_position_robo_hinten = act_position_robo_hinten.strip("\n""\r")

#         act_position_robo_vorne = tnblue.expect(["P11=".encode("ascii"), "ERROR".encode("ascii")], 1.0)
#         print(act_position_robo_vorne)
#         if "ERROR".encode("ascii") in act_position_robo_vorne:
#             tnblue.read_until("doesntmatter".encode("ascii"), 1.0)
#             exit()
#         else:
#             act_position_robo_vorne = tnblue.read_until("\n".encode("ascii"))
#             act_position_robo_vorne = act_position_robo_vorne.decode("ascii")
#             act_position_robo_vorne = act_position_robo_vorne.strip("\n""\r")

#         print("  Position Robo vorne" + Piezo_string) 
#         print("  Position Robob hinten" + cMUT_string)

#         time.sleep(0.2)

#          ###PXI
#         #sending command to start measurement to PXI    
#         UDP_connection_PXI(message_PXI_reached_position, response_PXI_reached_position)
        

#         #sending info about position to PXI 
#         act_postion= "Pos. Rob: Piezo: [" + act_position_robo_vorne + "] \t cMUT: [" + act_position_robo_hinten + "] \n \t"
#         send_points="Point Send: Piezo: " + Piezo_prestring + "\t cMUT: " + cMUT_prestring +" \n \t"
#         cMUT_position_std = np.array([cMUT_Points_np_std[b,0], cMUT_Points_np_std[b,1], cMUT_Points_np_std[b,2]])
#         Piezo_position_std = np.array([piezo_Points_np_std[a,0], piezo_Points_np_std[a,1], piezo_Points_np_std[a,2]])
#         std_points= "Std. Points: Piezo: " + str(Piezo_position_std) + "\t cMUT: " + str(cMUT_position_std) +"\n"

#         PXI_log= message_PXI_Log + "Number of MEAS:"+ str(current_measurment) + "\n \t" + send_points + act_postion + std_points
#         UDP_connection_PXI(PXI_log, response_PXI_Log)

#         # #Asking for Status of Measurement
#         UDP_connection_PXI(message_PXI_check_measure, response_PXI_check_measure)

#         ##controle via feedback to Robot
#         go= "0\r\n".encode("ascii")
#         tnblue.write(go)
#         tnred.write(go)

###End of measuerement##

# Bringing cMUT and Piezo to safety
# message_cMUT="P1 = 300.0 0.0 20.0 0.000 0 0 1\r\n".encode("ascii")
# message_Piezo="P1 = 300.0 0.0 20.0 0.000 0 0 1\r\n".encode("ascii")
# ## transfere of point data to Robo
# tnblue.write(message_Piezo)
# tnred.write(message_cMUT)
# ##control via Feedback from Robot
# confirmation_robo_vorne = tnblue.read_until("P11=".encode("ascii"))
# confirmation_robo_hinten = tnred.read_until("P11=".encode("ascii"))
# #controle via feedback to Robot
# go= "1\r\n".encode("ascii")
# tnblue.write(go)
# tnred.write(go)

# UDP_connection_PXI(message_PXI_end, response_PXI_end)
# number_of_measuerement = len(cMUT_Points_np) * len(piezo_Points_np)
# s.close()

# print(str(number_of_measuerement) + "Points have been measured")
# end_time=time.time()
# total_time=(end_time - start_time)/60
# total_time_round= round(total_time, 2)
# print("total time of measurement: " + str(total_time_round) + "min")