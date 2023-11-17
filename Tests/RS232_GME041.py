import serial
import csv
import serial.tools.list_ports
import time


def port_list():
    try:
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            print("No serial ports available for communication.")
        else:
            for port in ports:
                print(port)
    except serial.SerialException as e:
        print(f"An error occurred while listing the serial ports: {e}")


port_list()
ser = serial.Serial(
    "COM5", 9600
)  # Replace 'COM5' with your microcontroller's serial port


# Reception
try:
    # Read and print data from the microcontroller
    while True:
        data = ser.readline().decode("UTF-8").strip()
        print("Received string :", data)

except KeyboardInterrupt:
    # Close the serial port on Ctrl+C
    ser.close()
