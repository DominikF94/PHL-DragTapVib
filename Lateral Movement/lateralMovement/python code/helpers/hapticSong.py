import time
import serial
from helpers.stoppableThread import StoppableThread
from helpers.usbPorts import gloveUSB, ledUSB
from pygame import midi
from helpers.songs import getVibrationMessage


class pup(StoppableThread):
    def __init__(self, fullSong, songName, *args, **kwargs):
        self.song = fullSong
        self.songName = songName
        super(pup, self).__init__(*args, **kwargs)

    def run(self):
        midi.init()
        try:
            output = midi.Output(2)
        except Exception as e:
            print("Problem with keyboard output")
            print(e)
            exit()
        ser = serial.Serial(gloveUSB, 9600)
        time.sleep(3)
        print(self.song)
        while True:
            if self.stopped():
                return
            
            vibration_message = getVibrationMessage(self.song);
            ser.write((vibration_message+">").encode())
           # serLed = serial.Serial(ledUSB, 9600)
           # time.sleep(2)
           # serLed.write(self.songName.encode())
            time.sleep(1)
            i = 0
            song = self.song
            
            while i < len(song):
                if i > 0:
                    time.sleep(song[i][2]/1000)
                output.note_on(song[i][0], 80, 0)
                if i+1 != len(song) and song[i+1][2] == 0:
                    output.note_on(song[i+1][0], 80, 0)
                    time.sleep(song[i][1]/1000)
                    output.note_off(song[i][0], 0, 0)
                    output.note_off(song[i+1][0], 0, 0)
                    i = i+2
                else:
                    time.sleep(song[i][1]/1000)
                    output.note_off(song[i][0], 0, 0)
                    i = i+1
                
            time.sleep(1)
