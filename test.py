from importlib import reload
import importlib
import parameter
import move
import importlib

print(parameter.udp_messages.message_PXI_start)

importlib.reload(parameter)

print(parameter.udp_messages.message_PXI_start)