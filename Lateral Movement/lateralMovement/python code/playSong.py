from pygame import midi
from helpers.usbPorts import ledUSB, gloveUSB
import time
import serial
import sys
import getopt
from helpers.led_dictionary import notes_to_led
from helpers.led_dictionary import encodeLeds
from helpers.songs import getSongPart, getSongs, getVibrationMessage
from mido import MidiFile

from helpers.fileChecker import fileExists

pathPrefix = '/home/dominik/Masterarbeit/dataLearning'
id = 0
condition = ''
part = 0
attempt = 0
usage = "playSong.py -i id -c gold/gnew -p 1/2/3/4/12/34"
piece = ''
phrase = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hi:s:c:p:",
                               ["id=", "song" "condition=", "part="])
except getopt.GetoptError:
    print('playSong.py -i <id>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('test.py -i <id>')
        sys.exit()
    elif opt in ("-i", "--id"):
        if arg == "a":
            id = 2
        else:
            id = 1
#    elif opt  in ("-s", "--song"):
#        piece = arg
#        if piece == "a":
#            phrase = 0
#        elif piece == "b":
#            phrase = 1
#        else:
#            print("only Song a or b")
#            sys.exit(2)        
    elif opt in ("-p", "--part"):
        part = int(arg)
        if(part != 0 and part != 1 and
           part != 2 and part != 3 and
           part != 4 and part != 12 and part != 34):
            print("The session has to be either '1', '2', '3' or '4'")
            sys.exit()

if id == 0:
    print(usage)
    sys.exit()

if part == 0:
    songName, song = getSongs(id, "gnew")
else:
    songName, song = getSongPart(id, "gnew", part)
print("Hello")
print(songName)
print(song)
# songName_LED = songName
songName_LED = songName.split(":")[1]
led_message = encodeLeds(song);
#for note in song:
#    leds.append(str(notes_to_led.get(note[0])));
#led_message = ','.join(leds);
print(led_message);

KEYDOWN = 144
KEYUP = 128

midi.init()
try:
    output = midi.Output(2)
except Exception as e:
    print("Problem with keyboard output")
    print(e)
    exit()




#get serials for peripherials
serLed = serial.Serial(ledUSB, 9600)
serGlove = serial.Serial(gloveUSB, 9600)
time.sleep(2)
#send song to peripherilas
#serLed.write(songName_LED.encode())
serLed.write(led_message.encode())
vibration_message = getVibrationMessage(song);
print(vibration_message);
firstpart, secondpart = vibration_message[:len(vibration_message)//2], vibration_message[len(vibration_message)//2:]
#serGlove.write(firstpart.encode())
#serGlove.write((secondpart+'>').encode())
serGlove.write((vibration_message+'>').encode())
time.sleep(1)

notes_list_orig = []
i = 0
while i < len(song):
    if i > 0:
        time.sleep(song[i][2]/1000)
    output.note_on(song[i][0], 80, 0)
    # add note to list
    notes_list_orig.append(song[i][0])
    if i+1 != len(song) and song[i+1][2] == 0:
        output.note_on(song[i+1][0], 80, 0)
        notes_list_orig.append(song[i+1][0])
        time.sleep(song[i][1]/1000)
        output.note_off(song[i][0], 0, 0)
        output.note_off(song[i+1][0], 0, 0)
        i = i+2
    else:
        time.sleep(song[i][1]/1000)
        output.note_off(song[i][0], 0, 0)
        i = i+1
