import time
import serial
import random
from helpers.usbPorts import ledUSB, gloveUSB 

def generateSequence(length):
    return random.choices([6,7], k=length) 



ser = serial.Serial(gloveUSB, 9600)
seq = generateSequence(20)

print(seq)
if (input("Schreibe los zum Starten: ") == "los") :
    wert = 0
    test = 1
    while wert == 0:
        while test < 20 :
            val = 0 + test % 2
            val = str(val)
            print (val)
            ser.write(bytes(val, 'utf-8'))
            test = test +1
            time.sleep(1.5)
        print("Schreibe 0 um nochmal abwechselnd")
        wert =input()
        test = 1    
        
    while True:
        val = input()
        val = val
        print (val)
        ser.write(bytes(val, 'utf-8'))





