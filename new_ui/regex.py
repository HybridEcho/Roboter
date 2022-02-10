# test für Julian REGEX
import re
data_b = b'Welcome to RCX340\r\n\r\nP11=1 -170.916 9.995 32.331 0.000 0.000 1 0 0\r\nR:C:CURRENT_POSITION\r\n'
data_str = data_b.decode() # convert byte to string

data_str_split = data_str.split('P11')[1] # split str by "P11" .... HARDCODED! .... You aren't gonna need it (YAGNI)
# print(data_str_split)

num_values =  re.findall(r'[-+]?(?:\d*\.\d+|\d+)', data_str_split) # this is the magic.... erzähle ich dir morgen 

x = num_values[0]
y = num_values[1]
z = num_values[2]
r = num_values[3]

print("x", x, "y", y, "z", z, "r", r)