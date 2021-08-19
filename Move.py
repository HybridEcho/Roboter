#-ToDo:
#- Check settimeout Funktion scheint nicht zu funktionieren

from os import read
import telnetlib
import time
import numpy as np
import socket 
import parameter

#getting Pointfiles; Pointfiles musst contain a position for each Robot for each measurement, 
# Format: .csv with [x1,y1,z1] one point per line
# blue=Piezo=vorne  red=cMUT=hinten
cMUT_Points_np = np.atleast_2d(np.genfromtxt ("cMUT_Points.csv", delimiter=','))
piezo_Points_np = np.atleast_2d(np.genfromtxt ("Piezo_Points.csv", delimiter=','))
cMUT_Points_np_std = np.atleast_2d(np.genfromtxt ("cMUT_Points_std.csv", delimiter=','))
piezo_Points_np_std= np.atleast_2d(np.genfromtxt ("Piezo_Points_std.csv", delimiter=','))

def defining_connections (net_param):
    start_time = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(net_param.ip_local_socket, net_param.port_PXI)
    # #Festlegen der Ordernamen und Logfilenamen
    folder_name = input(":")
    parameter.udp_messages.set_folder_name(folder_name)

def UDP_connection(message, response):
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

def starting_RCX_move (tnblue, tnred):
    Meas_where="MOV\r\n".encode("ascii")
    tnblue.write(Meas_where)
    check_front = tnblue.read_until("Doesntmatter".encode("ascii"), 1.0)
    print(check_front)
    tnred.write(Meas_where)
    check_back =tnred.read_until("Doesntmatter".encode("ascii"), 1.0)
    print(check_back)


for a in range(len(piezo_Points_np)):
    for b in range(len(cMUT_Points_np)):
        number_of_measurements=len(cMUT_Points_np)*len(piezo_Points_np)
        current_measurment= (b+1 + a*len(cMUT_Points_np))
        print("Measurement " +str(current_measurment) + "of " + str(number_of_measurements))
        #line by line reading of csv file
        cMUT = np.array([cMUT_Points_np[b,0], cMUT_Points_np[b,1], cMUT_Points_np[b,2]])
        Piezo = np.array([piezo_Points_np[a,0], piezo_Points_np[a,1], piezo_Points_np[a,2]])

        ##transforming the single points to robo-readable format
        cMUT_prestring = np.array2string(cMUT, precision=3, separator=' ', floatmode='fixed', suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
        cMUT_string = cMUT_prestring.strip('['']')
        Piezo_prestring = np.array2string(Piezo, precision=3, separator=' ', floatmode='fixed',  suppress_small=True, formatter={'float_kind': '{: 0.10f}'.format})
        Piezo_string = Piezo_prestring.strip('['']')

        ##generation of the robo-message
        message_cMUT="P1 = ".encode("ascii") + cMUT_string.encode("ascii") + "0 0 0 1\r\n".encode("ascii")
        message_Piezo="P1 = ".encode("ascii") + Piezo_string.encode("ascii") + "0 0 0 1\r\n".encode("ascii")

        ## transfere of point data to Robo
        tnred.write(message_cMUT)
        tnblue.write(message_Piezo)

        ##control via Feedback from Robot
        act_position_robo_hinten = tnred.expect(["P11=".encode("ascii"), "ERROR".encode("ascii")], 1.0)
        print(act_position_robo_hinten)
        if "ERROR".encode("ascii") in act_position_robo_hinten :
            tnred.read_until("doesntmatter".encode("ascii"), 1.0)
            exit()
        else:
            act_position_robo_hinten = tnred.read_until("\n".encode("ascii"))
            act_position_robo_hinten = act_position_robo_hinten.decode("ascii")
            act_position_robo_hinten = act_position_robo_hinten.strip("\n""\r")

        act_position_robo_vorne = tnblue.expect(["P11=".encode("ascii"), "ERROR".encode("ascii")], 1.0)
        print(act_position_robo_vorne)
        if "ERROR".encode("ascii") in act_position_robo_vorne:
            tnblue.read_until("doesntmatter".encode("ascii"), 1.0)
            exit()
        else:
            act_position_robo_vorne = tnblue.read_until("\n".encode("ascii"))
            act_position_robo_vorne = act_position_robo_vorne.decode("ascii")
            act_position_robo_vorne = act_position_robo_vorne.strip("\n""\r")

        print("  Position Robo vorne" + Piezo_string) 
        print("  Position Robob hinten" + cMUT_string)

        time.sleep(0.2)

         ###PXI
        #sending command to start measurement to PXI    
        UDP_connection(message_PXI_reached_position, response_PXI_reached_position)
        

        #sending info about position to PXI 
        act_postion= "Pos. Rob: Piezo: [" + act_position_robo_vorne + "] \t cMUT: [" + act_position_robo_hinten + "] \n \t"
        send_points="Point Send: Piezo: " + Piezo_prestring + "\t cMUT: " + cMUT_prestring +" \n \t"
        cMUT_position_std = np.array([cMUT_Points_np_std[b,0], cMUT_Points_np_std[b,1], cMUT_Points_np_std[b,2]])
        Piezo_position_std = np.array([piezo_Points_np_std[a,0], piezo_Points_np_std[a,1], piezo_Points_np_std[a,2]])
        std_points= "Std. Points: Piezo: " + str(Piezo_position_std) + "\t cMUT: " + str(cMUT_position_std) +"\n"

        PXI_log= message_PXI_Log + "Number of MEAS:"+ str(current_measurment) + "\n \t" + send_points + act_postion + std_points
        UDP_connection(PXI_log, response_PXI_Log)

        # #Asking for Status of Measurement
        UDP_connection(message_PXI_check_measure, response_PXI_check_measure)

        ##controle via feedback to Robot
        go= "0\r\n".encode("ascii")
        tnblue.write(go)
        tnred.write(go)

###End of measuerement##

# Bringing cMUT and Piezo to safety
message_cMUT="P1 = 300.0 0.0 20.0 0.000 0 0 1\r\n".encode("ascii")
message_Piezo="P1 = 300.0 0.0 20.0 0.000 0 0 1\r\n".encode("ascii")
## transfere of point data to Robo
tnblue.write(message_Piezo)
tnred.write(message_cMUT)
##control via Feedback from Robot
confirmation_robo_vorne = tnblue.read_until("P11=".encode("ascii"))
confirmation_robo_hinten = tnred.read_until("P11=".encode("ascii"))
#controle via feedback to Robot
go= "1\r\n".encode("ascii")
tnblue.write(go)
tnred.write(go)

UDP_connection(message_PXI_end, response_PXI_end)
number_of_measuerement = len(cMUT_Points_np) * len(piezo_Points_np)
s.close()

print(str(number_of_measuerement) + "Points have been measured")
end_time=time.time()
total_time=(end_time - start_time)/60
total_time_round= round(total_time, 2)
print("total time of measurement: " + str(total_time_round) + "min")