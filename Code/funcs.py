############################################

#Linda Adams - Automatic Chord Estimation
#Chord finder function

###########################################

import numpy as np
from audiolazy import lazy_midi as lm

###################

def chord_finder(norm_window, sr, threshold):
    
    #index of first value above threshold
    idx = np.argmax(norm_window > threshold)
           
    #amount of frequencies in each bin if sr < 44100
    bin_resolution = sr / len(norm_window)
            
    #frequency of first value above threshold
    freq = idx * bin_resolution
    
    #get multiplication/scaling values for frequencies of each interval
    root_12 = 2 ** (1/12)
    scalar = sr/len(norm_window)
        
    #find ranges for each interval in the norm_window
    
    #minor 3rd
    m3_min = int((freq * (root_12**2.5)) / scalar)
    m3_max = int((freq * (root_12**3.5)) / scalar)
    m3_range = norm_window[m3_min:m3_max]

    #major 3rd
    ma3_min = int((freq * (root_12**3.5)) / scalar)
    ma3_max = int((freq * (root_12**4.5)) / scalar)
    ma3_range = norm_window[ma3_min:ma3_max]
        
    #perfect 4th
    p4_min = int(freq * ((root_12**4.5)) / scalar)
    p4_max = int(freq * ((root_12**5.5)) / scalar)
    p4_range = norm_window[p4_min:p4_max]

    #minor 7th        
    m7_min = int(freq * ((root_12**9.5)) / scalar)
    m7_max = int(freq * ((root_12**10.5)) / scalar)
    m7_range = norm_window[m7_min:m7_max]
        
    #major 7th  
    ma7_min = int(freq * ((root_12**10.5)) / scalar)
    ma7_max = int(freq * ((root_12**11.5)) / scalar)
    ma7_range = norm_window[ma7_min:ma7_max]

    #major 6th          
    ma6_min = int(freq * ((root_12**8.5)) / scalar)
    ma6_max = int(freq * ((root_12**9.5)) / scalar)
    ma6_range = norm_window[ma6_min:ma6_max]

    #major 9th          
    ma9_min = int(freq * ((root_12**13.5)) / scalar)
    ma9_max = int(freq * ((root_12**14.5)) / scalar)
    ma9_range = norm_window[ma9_min:ma9_max]

    #minor 9th           
    m9_min = int(freq * ((root_12**12.5)) / scalar)
    m9_max = int(freq * ((root_12**13.5)) / scalar)
    m9_range = norm_window[m9_min:m9_max]
    
    #augmented 9th       
    aug9_min = int(freq * ((root_12**14.5)) / scalar)
    aug9_max = int(freq * ((root_12**15.5)) / scalar)
    aug9_range = norm_window[aug9_min:aug9_max]
        
        
    #scale thresholds for higher frequencies, as amplitudes with be lower
    third_thresh = threshold * 0.5
    seventh_thresh = threshold * 0.25
    ninth_thresh = threshold * 0.000001
        
    #check for highest amplitude for thirds frequencies and check against threshold
    third_array = ([np.max(m3_range), np.max(ma3_range), np.max(p4_range)])
    third_type = np.argmax(third_array)
    if np.max(third_array) > third_thresh:
        third = True        
    else: third = False
            
    #check for highest amplitude for sevenths frequencies and check against threshold
    seventh_array = ([np.max(m7_range), np.max(ma7_range), np.max(ma6_range)])
    seventh_type = np.argmax(seventh_array)
    if np.max(seventh_array) > seventh_thresh:
        seventh = True
    else: seventh = False
            
    #check for highest amplitude for ninths frequencies and check against threshold
    ninth_array = ([np.max(m9_range), np.max(ma9_range), np.max(aug9_range)])
    ninth_type = np.argmax(ninth_array)
    if np.max(ninth_array) > ninth_thresh:
        ninth = True
    else: ninth = False
    
    
    #narrow down chord_types by chord_type tones
    if third:
        if third_type == 0:
            chord_type = " Minor"
        elif third_type == 1:
            chord_type = " Major"
        elif third_type == 2:
            chord_type = " Sus"
    else:
        chord_type = " Undefined"
    
        
    if chord_type == " Minor" and seventh:
        if seventh_type == 0:
            chord_type = " Minor 7"
        elif seventh_type == 1:
            chord_type = " Minor Major 7"
        elif seventh_type == 2:
            chord_type = " Minor 6"
    
    elif chord_type == " Major" and seventh:
        if seventh_type == 0:
            chord_type = " Dominant 7"
        elif seventh_type == 1:
            chord_type = " Major 7"
        elif seventh_type == 2:
            chord_type = " Major 6"    
            
    elif chord_type == " Sus" and seventh:
        if seventh_type == 0:
            chord_type = " Dominant 7 sus"
                               
    if chord_type == " Minor 7" and ninth:
        if ninth_type == 1:
            chord_type = " Minor 9"
        
    elif chord_type == " Major 7" and ninth:
        if ninth_type == 1:
            chord_type = " Major 9"
       
    elif chord_type == " Dominant 7" and ninth:
        if ninth_type == 0:
            chord_type = " Dominant 7 b9"
        elif ninth_type == 1:
            chord_type = " Dominant 9"
        elif ninth_type == 2:
            chord_type = " Dominant 7 #9"  
        
    elif chord_type == " Dominant 7 Sus" and ninth:
        if ninth_type == 1:
            chord_type = " Dominant 9 sus"
            
    elif chord_type == " Major 6" and ninth:
        if ninth_type == 1:
            chord_type = " Major 6/9"
            
    elif chord_type == " Minor 6" and ninth:
        if ninth_type == 1:
            chord_type = " Minor 6/9"
     
    #get chord names    
    root_name_full = lm.freq2str(freq)
    root_name = root_name_full[0:3]
    chord_name = root_name + chord_type
    
    return chord_name
