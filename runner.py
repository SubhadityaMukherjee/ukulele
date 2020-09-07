# %%
import librosa
import numpy as np
import scipy
import scipy.io.wavfile as wv
import argparse
import os
#%%
parser = argparse.ArgumentParser()
parser.add_argument("-d","--dir", help="Directory to get audio from", default = "music/")
parser.add_argument("-r", "--rate", help="Audio rate", default = 22040, type = int)
parser.add_argument("-o", "--order", help="Audio Progression", type = str)
parser.add_argument("-f", "--fname", help="Output file name", type = str)
args = parser.parse_args()

# %%
music = [args.dir+x for x in os.listdir(args.dir)]
chords = [x.split(".")[0] for x in music]

# %%

def loadsong(x):
    """
    Removes zeros from before an after
    Returns an array with the audio
    """
    return np.trim_zeros(librosa.load(x, sr=None)[0])

#%%
def indivsplit(x):
    """
    Splits by * to find out number of repeats
    If no * then returns 1 repeat
    Returns the folder directly to save time
    """
    temp = x.split("*")
    try:
        rep = int(temp[1])
    except IndexError or ValueError:
        rep = 1

    return f"{args.dir}{str(temp[0])}.wav", rep

#%%
def musicloader(tup):
    """
    Goes through all audio mentioned
    Loads them once for more efficiency
    Takes the repeat number for each audio clip, repeats it that many times
    Merges as one audio and returns an array with that
    """
    songs = list(set([x[0] for x in tup]))
    songs_all = [x[0] for x in tup]
    rep = [x[1] for x in tup]
    dict_songs = {x:loadsong(x) for x in songs}
    mix_song = []
    for i in range(len(rep)):
        assert len(tup) == len(rep)
        mix_song.extend(np.tile(dict_songs[songs_all[i]], rep[i]))
    print("[INFO] Done! Check the output folder")
    return np.array(mix_song)
    

#%%

def chordprogression(x):
    """
Write the chords separated by ; and -number to denote how many times
If no number is specified then it will be taken once.
eg. am-2;b-3;b;bm-10
"""
    chords = x.split(";")
    read_chords = [indivsplit(chord) for chord in chords]
    print(f"[INFO] Read all chords : {read_chords}")
    return read_chords
#%%
def repeater(x, n):
    """
    Repeats an array n times and concatenates them
    """
    return np.tile(x, n)

# %%
cp = chordprogression(args.order)
# %%

wv.write(f"{args.fname}.wav", int(args.rate), musicloader(cp))
# %%