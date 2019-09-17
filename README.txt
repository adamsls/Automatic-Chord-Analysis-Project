
To run the chord estimation algorithm, open main.py, funcs.py and setup.py from the Code folder

In main.py, add a .wav file to be analysed (sample wavs are included in
the folder 'Sample Chords'). A default chord (C7sus) has been entered, which is contained in the file directory.The algorithm will only run on fairly short segments of a single instrument playing root position chords. 

Then, set the sample rate, which can be long since the time resolution 
does not need to be particularly sharp, given that chords are generally
longer than 22050 samples at 44100Hz sample rate. 

Finally, run the file main.py. The contents of an array will be printed to the console. The array contains the per-fft-window analysis of the harmony in each window. 