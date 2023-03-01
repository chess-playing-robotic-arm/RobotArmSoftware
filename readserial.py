import serial

arduino_port = "COM3"
baud = 9600
fileName = "analog-data.csv"
samples = 10
print_labels = False

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port: ", arduino_port)
file = open(fileName, "a")
print("Created file")

line = 0

while line <= samples:
    if print_labels:
        if line==0:
            print("Printing Column Headers")
        else:
            print("Line " + str(line) + ": writing...")

    getData=str(ser.readLine())
    data=getData[0:][:-2]
    print(data)

    file = open(fileName, "a")     

ser.close()       