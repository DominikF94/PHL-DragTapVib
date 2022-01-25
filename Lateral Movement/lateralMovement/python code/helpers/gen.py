import songs
import led_dictionary

def genSong(name, fullSong,b, e):

    print()
    print(f"void {name}() " + "{")
    print()
    i = 0
    song = fullSong[b:e]
    while i < len(song):
        print(f"// note {i+1}")
        print(f"leds[{led_dictionary.notes_to_led.get(song[i][0])}] = CRGB(5, 0, 0);")
        if i+1 != len(song) and song[i+1][2] == 0:
            print(f"leds[{led_dictionary.notes_to_led.get(song[i+1][0])}] = CRGB(5, 0, 0);")
            print("FastLED.show();")
            print(f"delay({song[i][1]});")
            print(f"leds[{led_dictionary.notes_to_led.get(song[i][0])}] = CRGB(0, 0, 0);")
            print(f"leds[{led_dictionary.notes_to_led.get(song[i+1][0])}] = CRGB(0, 0, 0);")
            print(f"delay({song[i][2]});")
            i = i+1
        else:
            print("FastLED.show();")
            print(f"delay({song[i][1]});")
            print(f"leds[{led_dictionary.notes_to_led.get(song[i][0])}] = CRGB(0, 0, 0);")
            print(f"delay({song[i][2]});")
        i = i+1
    print("FastLED.show();")
    print("}")
    print()

def genSongB():
    genSong("songB", songs.fullSongB,0, 25)
    genSong("songB_1", songs.fullSongB,0, 7)
    genSong("songB_2", songs.fullSongB,7, 14)
    genSong("songB_3", songs.fullSongB,14, 21)
    genSong("songB_4", songs.fullSongB, 21, 25)
    genSong("songB_12", songs.fullSongB, 0, 14)
    genSong("songB_34", songs.fullSongB, 14, 25)

def genSongA():
    genSong("songA", songs.fullSongA,0, 22)
    genSong("songA_1", songs.fullSongA,0, 4)
    genSong("songA_2", songs.fullSongA,4, 8)
    genSong("songA_3", songs.fullSongA,8, 14)
    genSong("songA_4", songs.fullSongA,14, 22)
    genSong("songA_12", songs.fullSongA, 0, 8)
    genSong("songA_34", songs.fullSongA, 8, 22)

def figMot (fig):
    if fig == 1:
        return "motorPin12"
    if fig == 2:
        return "motorPin7"
    if fig == 3:
        return "motorPin4"
    if fig == 4:
        return "motorPin2"
    if fig == 5:
        return "motorPin3"

def figMot_helper(key, nextkey):
    if key > nextkey:
        return "motorPin10"
    else:
        return "motorPin8"

songBbreaks = [4, 11, 17, 22]

def genMotSong (name, fullSong,b,e, songBreaks):
    print()
    print(f"void {name}() " + "{")
    print()
    i = 0
    song = fullSong[b:e]
    while i < len(song):
        print(f"    // note {i+1}")
        if i > 0:
            print(f"    delay({song[i][2]});")
        print(f"    digitalWrite({figMot(song[i][3])}, HIGH);")
        if i+1 != len(song) and song[i+1][2] == 0:
            print(f"    digitalWrite({figMot(song[i+1][3])}, HIGH);")
            if i+1 in songBreaks:
                print(f"    delay(489);")
            else:
                print(f"    delay({song[i][1]});")
            print(f"    digitalWrite({figMot(song[i][3])}, LOW);")
            print(f"    digitalWrite({figMot(song[i+1][3])}, LOW);")
            if i+1 in songBreaks:
                print("    if (con) {")
                print(f"        digitalWrite({figMot_helper(song[i][3],song[i+1][3])}, HIGH);")
                print(f"        delay(400);")
                print(f"        digitalWrite({figMot_helper(song[i][3],song[i+1][3])}, LOW);")
                print(" } else {")
                print(f"        delay(400);")
                print("}")
            i = i+1
        else:
            if i in songBreaks:
                print(f" delay(489);")
            else:
                print(f"    delay({song[i][1]});")
            print(f"    digitalWrite({figMot(song[i][3])}, LOW);")
            if i in songBreaks:
                print("    if (con) {")
                print(f"        digitalWrite({figMot_helper(song[i][3],song[i+1][3])}, HIGH);")
                print(f"        delay(400);")
                print(f"        digitalWrite({figMot_helper(song[i][3],song[i+1][3])}, LOW);")
                print(" } else {")
                print(f"        delay(400);")
                print("}")
        i = i+1
    print("}")
    print()

def genSongB_mot():
    genMotSong("songB", songs.fullSongB,0, 25, songBbreaks)
    genMotSong("songB_1", songs.fullSongB,0, 7, songBbreaks)
    genMotSong("songB_2", songs.fullSongB,7, 14, songBbreaks)
    genMotSong("songB_3", songs.fullSongB,14, 21, songBbreaks)
    genMotSong("songB_4", songs.fullSongB, 21, 25, songBbreaks)
    genMotSong("songB_12", songs.fullSongB, 0, 14, songBbreaks)
    genMotSong("songB_34", songs.fullSongB, 14, 25, songBbreaks)

def genSongA_mot():
    genMotSong("songA", songs.fullSongA,0, 22, songBbreaks)
    genMotSong("songA_1", songs.fullSongA,0, 4, songBbreaks)
    genMotSong("songA_2", songs.fullSongA,4, 8, songBbreaks)
    genMotSong("songA_3", songs.fullSongA,8, 14, songBbreaks)
    genMotSong("songA_4", songs.fullSongA, 14, 22, songBbreaks)
    genMotSong("songA_12", songs.fullSongA, 0, 8, songBbreaks)
    genMotSong("songA_34", songs.fullSongA, 8, 22, songBbreaks)

genSongB_mot()
#genSongB()
#genSongA()
genSongA_mot()
