############################################

#Linda Adams - Automatic Chord Estimation
#Main

###########################################

import numpy as np
import librosa

import funcs
import setup


###################USER INPUT########################

#1) Choose audio file to import for chord-finding
#Samples wavs can be found in Sample Chords folder (input must be single instrument root position chords)
#
signal, sr = librosa.load('C7sus.wav', mono = True, sr = None)

#2) Choose fft_size: recommended - between 11,025 and 44,100 (as chords move slower than melody)
fft_size = 44100

#3) Run file and view printed progression array
#Contains chords in each window (at 120bpm 44100 fft-size = 2 beats per chord window)

#END OF USER INPUT############################################







#Call function to get fft
abs_fft_signal, threshold = setup.do_fft(signal, fft_size)

#Array to contain resulting chords
progression_array = []


#Call function analyse chords in each window
for window in abs_fft_signal:

    #normalise
    norm_window = librosa.util.normalize(window)
    
    thresh_norm_window = np.array([norm_window > threshold])
    
    if thresh_norm_window.any():
        chord_name = funcs.chord_finder(norm_window, sr, threshold)
        
    else:
        chord_name = ""
        
    progression_array.append(chord_name)
    
print(progression_array)
