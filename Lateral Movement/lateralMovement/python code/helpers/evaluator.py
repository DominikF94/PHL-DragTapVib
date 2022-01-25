from time import daylight
import mido
from mido.midifiles.units import tempo2bpm
from songs import getSongPath
from dwt_hard import compareSongs, midiToArrayVer2, midiToArrayVer1, dtwLists, dtw
import sys, getopt
from fileChecker import fileExists
from mido.midifiles.midifiles import MidiFile



def displayMidi(song):
    osong = MidiFile(song)
    tpb = osong.ticks_per_beat
    for i, track in enumerate(osong.tracks):
        #print(track)
        notesArray = []
        print('Track {}: {}'.format(i, track.name))
        notesPressed = []
        notesReleased = []
        abs = 0
        for msg in track:
            diff =  mido.tick2second(msg.time,tpb, tempo)
            abs = abs + diff
            #print(msg, ' Abs = ' + str(round(abs, 3)) + ' Diff= ' + str(round(diff, 3)))
            if (msg.type == "note_on" and msg.velocity > 0 and msg.time != 0):
                notesPressed.append(msg.note)
            if (msg.type == "note_on" and msg.velocity == 0):
                notesReleased.append(msg.note)
                if (len(notesPressed) == len(notesReleased)):
                    notesArray.append(notesPressed)
                    notesPressed = []
                    notesReleased = []
        #print(notesArray)
        return notesArray


def midiToArrWithTimes(song):
    osong = MidiFile(song)
    tpb = osong.ticks_per_beat
    for i, track in enumerate(osong.tracks):
        notesStarted = []
        result = []
        abs = 0
        for msg in track:
            diff =  mido.tick2second(msg.time,tpb, tempo)
            abs = abs + diff
            if (msg.type == "note_on" and msg.velocity > 0 and msg.time != 0):
                note = (msg.note, abs, 0)
                notesStarted.append(note)
            if (msg.type ==  "note_off"):
                for note in notesStarted:
                    if note[0] == msg.note:
                        toAdd = (note[0], note[1], abs)
                        notesStarted.remove(note)
                        result.append(toAdd)
    return result


def midiToArrOverlaps(arrWithTimes):
    #print(arrWithTimes)
    overlaps = []
    print(arrWithTimes)

    for i in range (0, len(arrWithTimes) - 2):
        #print (  arrWithTimes[i+1][1], arrWithTimes[i][2])
        #overlap is time that (Negative Overlap means that the notze after starts this time before tis on ends)
        overlap = arrWithTimes[i+1][1] - arrWithTimes[i][2]
        #print (arrWithTimes[i][0], overlap)
        note = (arrWithTimes[i][0], overlap)
        overlaps.append(note)
    overlaps.append((arrWithTimes[len(arrWithTimes)-1][0], 0) )

    return overlaps

# overlap is the time a note starts before the one before ends (-0,1 means note starts 0.1 s before the other ends)
def midiToArrCut(arrWithOverlap, overlap):
    #print(arrWithOverlap)
    arr = []
    overlapping = []
    for notes in arrWithOverlap:
        #print(notes[1])
        if (notes[1] <  overlap):
            overlapping.append(notes[0])
            arr.append(overlapping)
            overlapping = []
        else :
            #print("hier")
            overlapping.append(notes[0])
    return arr

def midiToArr(song, overlap):
    list = midiToArrOverlaps(midiToArrWithTimes(song))
    list = midiToArrCut(list, overlap)
    return list
    


def compareSongs2(originalSong, testedSong, overlap):
    original_song = MidiFile(originalSong)
    test_song = MidiFile(testedSong)
    test = dtwLists(midiToArrayVer2(original_song), midiToArr(testedSong, overlap), dist=dtw)
    return test


tempo = 500000
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
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
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

path = pathPrefix + str(id) + '/' + piece + '_' + condition + '/'  + session + '/'

if(fileExists(path+attempt+".mid")):
    print("file exists")
else:
    print
    print ("file doesn't exist")


originalSong = getSongPath(song, condition)
#print(originalSong)
played = path + attempt + ".mid"
compare = compareSongs(originalSong, played)
print(compare)
file = open(path + attempt + "_eval1.txt", "w")
midiplayed= MidiFile(played)
midiArr = midiToArrayVer1(midiplayed)
print("Hello" ,midiArr)

#displayMidi(played)

file.write(condition + "\n Orig: " + str(midiToArrayVer2(MidiFile(originalSong))) +"\n Played:" +  str(midiArr) +"\n" + str(compare))
file.close

times = midiToArrWithTimes(played)
over = midiToArrOverlaps(times)
#print(midiplayed.tracks)
#cleand = midiToArr(over)
midiToArrayVer2(MidiFile(originalSong))
midiToArrayVer1(midiplayed)
compare = compareSongs2(originalSong, played, 0.25)

print(compare)
#print (cleand)
