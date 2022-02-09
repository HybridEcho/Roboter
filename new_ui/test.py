import telnetlib

tnblue = telnetlib.Telnet(b"192.168.33.10")
tnblue.write("C:R:SERVO_OFF\r\n".encode("ascii"))
w=tnblue.read_until(b"test", 1)
print(w)
print("t2")