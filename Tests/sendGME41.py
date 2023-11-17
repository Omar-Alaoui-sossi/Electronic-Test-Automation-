import serial

from time import localtime, strftime

ser = serial.Serial()

ser.port = "COM5"

ser.baudrate = 19200

ser.open()

# temp_file = open("temp_humid.txt", "a", encoding="utf-8")

while True:
    ser.write("hello".encode("utf-8"))
    line = ser.readline()

    print(line)

    # temp_file.write(strftime("%d %b %Y %H%M%S ", localtime()))

    # temp_file.write(line.decode())
