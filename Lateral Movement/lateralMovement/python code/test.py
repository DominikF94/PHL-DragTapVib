import sys, getopt
import subprocess
import signal
import os

from mido.midifiles.midifiles import MidiFile
from helpers.dwt_hard import compareSongs, midiToArrayVer1, midiToArrayVer2
from helpers.fileChecker import fileExists, existsDirectory, createPath
from helpers.songs import getSongPath

if (os.system('arecordmidi -l | grep CASIO') != 0):
    print("Piano is not connect")
    sys.exit()

usage = 'test.py -i <id> -p <piece> -a <attempt> -c <condition> -s <session>'
id = 0
attempt = ""
condition = ""
session = ''
piece =''
song = ''
pathPrefix = '/home/dominik/Masterarbeit/data/'
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:p:a:c:s:",["id=","piece=","attpemt=","condition=","session="])
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(usage)
        sys.exit()

    elif opt  in ("-p", "--peace"):
        piece = arg
        if piece == "a":
            song = 0
        elif piece == "b":
            song = 1
        else:
            print("only Song a or b")
            sys.exit(2)
    elif opt in ("-i", "--id"):
        try:
            id = int(arg)
        except Exception as e:
            print("id was not an integer")
    elif opt in ("-a", "--attpemt"):
        attempt = arg
    elif opt in ("-c", "--condition"):
        condition = arg
        if(condition != "gold" and condition != "gnew"):
            print("The condition has to be either 'gold' or 'gnew'")
            sys.exit()
    elif opt in ("-s", "--session"):
        session = arg
        if(session != "pretest" and session != "posttest" and session != "test"):
            print("The session has to be either '1' or '2'")
            sys.exit()

if (id == 0 and attempt == "" and condition == "" and sessiont == ""):
    print(usage)
    sys.exit()

path = pathPrefix + str(id) + '/' + piece + '_' + condition + '/'  + session + '/';
#check if file exists
print(piece)
if(fileExists(path+attempt+".mid")):
    print("file exists")
    sys.exit()
if(existsDirectory(path) != True):
    print("dir has to be created")
    createPath(path)

port = subprocess.Popen("arecordmidi -l |  awk '$2 ~ /CASIO/ {print $1}'", shell=True, stdout=subprocess.PIPE)
x = subprocess.Popen('arecordmidi -p ' +
                     port.stdout.read().decode("utf-8").rstrip() +
                     ' ' + path +
                     attempt + ".mid",
                     shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

print("Started Capture")
print("Press Enter to Stop Capture")
print(path)
input()
print("Stopping Capture")
os.killpg(os.getpgid(x.pid), signal.SIGTERM)
originalSong = getSongPath(song, condition)
print(originalSong)
justPlayed = path + attempt + ".mid"
compare = compareSongs(originalSong, justPlayed)
print(compare)
file = open(path + attempt + ".txt", "w")
played = midiToArrayVer2(MidiFile(justPlayed))
file.write(condition + "\n Orig: " + str(midiToArrayVer2(MidiFile(originalSong))) +"\n Played:" +  str(played) +"\n" + str(compare))
file.close

