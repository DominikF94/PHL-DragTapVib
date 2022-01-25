#Test dtw
#Based on https://github.com/pierre-rouanet/dtw
from math import isinf
from numpy import array, zeros, full, argmin, inf, ndim
import numpy as np
from mido import MidiFile

def dtw(x, y, dist, warp=1, w=inf, s=1.0):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    :param func dist: distance used as cost measure
    :param int warp: how many shifts are computed.
    :param int w: window size limiting the maximal distance between indices of matched entries |i,j|.
    :param float s: weight applied on off-diagonal moves of the path. As s gets larger, the warping path is increasingly biased towards the diagonal
    Returns the minimum distance
    """
    assert len(x)
    assert len(y)
    assert isinf(w) or (w >= abs(len(x) - len(y)))
    assert s > 0
    r, c = len(x), len(y)
    if not isinf(w):
        D0 = full((r + 1, c + 1), inf)
        for i in range(1, r + 1):
            D0[i, max(1, i - w):min(c + 1, i + w + 1)] = 0
        D0[0, 0] = 0
    else:
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if (isinf(w) or (max(0, i - w) <= j <= min(c, i + w))):
                D1[i, j] = dist(x[i], y[j])
    jrange = range(c)
    for i in range(r):
        if not isinf(w):
            jrange = range(max(0, i - w), min(c, i + w + 1))
        for j in jrange:
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
            D1[i, j] += min(min_list)
    return D1[-1, -1]

def dtwLists(x, y, dist, warp=1, w=inf, s=1.0):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    :param func dist: distance used as cost measure
    :param int warp: how many shifts are computed.
    :param int w: window size limiting the maximal distance between indices of matched entries |i,j|.
    :param float s: weight applied on off-diagonal moves of the path. As s gets larger, the warping path is increasingly biased towards the diagonal
    Returns the minimum distance
    """
    assert len(x)
    assert len(y)
    assert isinf(w) or (w >= abs(len(x) - len(y)))
    assert s > 0
    r, c = len(x), len(y)
    if not isinf(w):
        D0 = full((r + 1, c + 1), inf)
        for i in range(1, r + 1):
            D0[i, max(1, i - w):min(c + 1, i + w + 1)] = 0
        D0[0, 0] = 0
    else:
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if (isinf(w) or (max(0, i - w) <= j <= min(c, i + w))):
                custom_distance = lambda x, y: 0 if x==y else 1
                D1[i, j] = dist(x[i], y[j], dist=custom_distance)
    jrange = range(c)
    for i in range(r):
        if not isinf(w):
            jrange = range(max(0, i - w), min(c, i + w + 1))
        for j in jrange:
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
            D1[i, j] += min(min_list)
    return D1[-1, -1]

def midiToArrayVer1(mid):

    for i, track in enumerate(mid.tracks):
        notesArray = []
        print('Track {}: {}'.format(i, track.name))
        notesPressed = []
        notesReleased = []
        for msg in track:
            if (msg.type == "note_on" and msg.time != 0):
                notesPressed.append(msg.note)
            if (msg.type == "note_off" and msg.time != 0):
                notesReleased.append(msg.note)
                if (len(notesPressed) == len(notesReleased)):
                    notesArray.append(notesPressed)
                    notesPressed = []
                    notesReleased = []
        for entries in notesArray:
            entries.sort()
        print(notesArray)
        return notesArray


def midiToArrayVer2(mid):
    for i, track in enumerate(mid.tracks):
        notesArray = []
        print('Track {}: {}'.format(i, track.name))
        notesPressed = []
        notesReleased = []
        for msg in track:
            if (msg.type == "note_on" and msg.velocity > 0):
                notesPressed.append(msg.note)
            if (msg.type == "note_on" and msg.velocity == 0):
                notesReleased.append(msg.note)
                if (len(notesPressed) == len(notesReleased)):
                    notesArray.append(notesPressed)
                    notesPressed = []
                    notesReleased = []
        print(notesArray)
        return notesArray

def compareSongs(originalSong, testedSong):
    original_song = MidiFile(originalSong)
    test_song = MidiFile(testedSong)
    test = dtwLists(midiToArrayVer2(original_song), midiToArrayVer1(test_song), dist=dtw)
    return test


def compareSongs2(originalSong, testedSong):
    original_song = MidiFile(originalSong)
    test_song = MidiFile(testedSong)
    test = dtwLists(midiToArrayVer2(original_song), midiToArrayVer1(test_song), dist=dtw)
    return test
