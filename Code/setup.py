############################################

#Linda Adams - Automatic Chord Estimation
#FFT

###########################################

import numpy as np
from scipy.fftpack import fft
import librosa
from skimage import util
import statistics as st

#############################

def do_fft(signal, fft_size):
    
    #thresholding and normalisation
    threshold_fft = fft(signal)
    
    #take absolute values and round
    rounded_freq = np.round(abs(threshold_fft))
    
    #normalise
    norm_rounded_freq = librosa.util.normalize(rounded_freq)
    
    #find most common rounded value in case of high noise floow
    mode_freq = st.mode(norm_rounded_freq)
                
    #threshold is noise floor plus 0.5
    threshold = (mode_freq) + 0.5
    
    ##########################
    
    #FFT

    #slice into segments
    slices = util.view_as_windows(signal, window_shape=(fft_size,), step=fft_size)
    
    #use hanning window on segments
    win = np.hanning(fft_size + 1)[:-1]
    
    #multiply slices by hanning window
    slices_win = slices * win
    
    #add interpolated zeros after fft
    zero_padding = int(fft_size * 1.125)
    
    #do fft
    fft_signal = fft(slices_win, zero_padding)
    
    #take absolute values
    abs_fft_signal = np.abs(fft_signal)
       
    return abs_fft_signal, threshold
