notes_to_led = {
60 : 47,#,48
64 : 54,#,55
65 : 57,#,58
67 : 61,
69 : 64,#,65
71 : 68,
72 : 71,
74 : 74,#,75
76 : 77,#,78
77 : 81,
79 : 84,#,85
81 : 88,
83 : 91,
84 : 94#,95
}

def encodeLeds(song):
    i = 0
    leds = [];
    while i < len(song):
        ledsAtTheSameTime = [];
        ledsAtTheSameTime.append(str(notes_to_led.get(song[i][0])));
        if i+1 != len(song) and song[i+1][2] == 0:
            ledsAtTheSameTime.append(str(notes_to_led.get(song[i+1][0])));
            i = i+2
        else:
            i = i+1
        leds.append(';'.join(ledsAtTheSameTime));
    return ','.join(leds);
