import serial
import random


def generateSequence(length):
    return random.choices([0,1], k=length) 



ser = serial.Serial('/dev/ttyACM2', 9600)
seq = generateSequence(20)

print(seq)
if (input("Schreibe los zum Starten: ") == "los") :
    for i in range(1, len(seq) + 1) :
        val = input("Nr. {number}, Direction {dir}: ".format(number = i, dir= seq[i - 1]))
        dir = str(seq[i-1])
        ser.write(bytes(dir, 'utf-8'))

