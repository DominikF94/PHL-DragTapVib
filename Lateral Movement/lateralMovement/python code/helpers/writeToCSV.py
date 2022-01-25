import csv
import os
import re
import dwt_hard
import songs
from mido.midifiles.midifiles import MidiFile

dirname = "/home/dominik/Masterarbeit/data/"

filename = 'Results.csv'
fields = ['ID', 'Order', 'Avg. Test New', 'Avg. Posttest New', 'DiffNew',
    'Avg Test old', 'Avg. Posttest old', 'Diff old', 'Diff old-new', 'Pre-New', 'T1-New' ,'T2-New', 'T3-New', 'P1-New', 'P2-New', 'P3-New', 'P4-New', 'P5-New', 'P6-New', 'Pre-Old', 'T1-Old' ,'T2-Old', 'T3-Old', 'P1-Old', 'P2-Old', 'P3-Old', 'P4-Old', 'P5-Old', 'P6-Old']
numbers = re.compile(r'\d+(?:\.\d+)?')


rows = [[]]


def analyzeMidiList(midiList, song):
    values = []
    for midi in midiList:
        print(midi)
        val = dwt_hard.compareSongs(songs.getSongPath(song, 'gold'), midi)
        values.append(val)

    return values


def listMidiFiles(dir):
    midiFiles = []
    # return all files as a list
    for file in os.listdir(dir):
     # check the files which are end with specific extension
        if file.endswith(".mid"):
        # print path name of selected files
            midiFiles.append(os.path.join(dir, file))

    return sorted(midiFiles)


def getListofAttempts(dir, song):
    string = ""
    list = []
    pre = []
    test = []
    post = []
    for file in os.listdir(dir):
        if 'pretest' == str(file):
            midiList = listMidiFiles(os.path.join(dir, file))
            string = string + "preTest \n" + getPlayeList(midiList)
            pre = analyzeMidiList(midiList, song)
            assert(len(pre)==1)
        if 'test' == str(file):
            midiList = listMidiFiles(os.path.join(dir, file))
            test = analyzeMidiList(midiList, song)
            string = string + "Test \n" + getPlayeList(midiList)
            assert(len(test)==3)
        if 'posttest' == str(file):
            midiList = listMidiFiles(os.path.join(dir, file))
            string = string + "postTest \n" + getPlayeList(midiList)
            post = analyzeMidiList(midiList, song)
            if len(post) !=6:
                post.append(-1)
                assert(len(post)==6)
    file = open(dir + "attempts.txt", "w")
    file.write(string)
    file.close()
    list = pre + test + post
    return list


def getRow (id, folder):
    row = [id, 'order', 0 , 0, 0,0,0,0,0]
    newRes=[]
    # /home/data/i/ ==> Die folder , der Versuche  (A_GNEW...)
    Parts = getDirsInFolder(folder)
    resultsNew = []
    resultsOld = []
    for dir in Parts:
        print(dir)
        song = 0
        if 'b_' in str(dir):
            song = 1
        #Bei Verwendung neues Dir
        #print(song)
        if 'new' in str(dir):
            resultsNew = getListofAttempts(dir, song)
        else :
            print(song)
            resultsOld = getListofAttempts(dir, song)
    row = row + resultsNew
    row = row + resultsOld
    
    return row


def getPlayeList(midis):
    playedSongs = ""
    print("Hier" , midis)
    for midi in midis:
        print (midi)
        playedSongs = playedSongs + str(dwt_hard.midiToArrayVer1(MidiFile(midi))) + "\n"
    return playedSongs
    
                    


def getDirsInFolder(dir):
    dirfiles = os.listdir(dir)
    fullpaths = map(lambda name: os.path.join(dir, name), dirfiles)
    dirs = []
    for file in fullpaths:
        if os.path.isdir(file):dirs.append(file)
    dirs = sorted(dirs)
    return dirs


probands = getDirsInFolder(dirname)
with open(dirname + 'Results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fields)
    for i in range(0, len(probands)):
        curPath = numbers.findall(str(probands[i]))
        if len(curPath) != 0:
            id = str(numbers.findall(str(probands[i])).pop())
            id = int(id)
            writer.writerow(getRow(id, probands[i]))




