# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass


#!/usr/bin/python3
import time
import serial
import os
from motor_controll import motor_cmd


print("UART")
print("NVIDIA Jetson Xavier Developer Kit")


serial_port = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

get_commands = motor_cmd()
print(get_commands.forward())

# command = input("Send command:")
# print(command, "sent.")
try:
    # Send a simple header
    serial_port.write(get_commands.foward().encode()) #\r\n
    # serial_port.write("Ntst\r\n".encode())
    while True:
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            print(data)
            # serial_port.write(data)
            # if we get a carriage return, add a line feed too
            # \r is a carriage return; \n is a line feed
            # This is to help the tty program on the other end
            # Windows is \r\n for carriage return, line feed
            # Macintosh and Linux use \n
            #if data == "\r".encode():
                # For Windows boxen on the other end

             # denne sender feedback fra motor ut igjen til motor så det looper
             #   serial_port.write("\n".encode())


except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
# sudo python3 UART_Python.py for å kjøre






