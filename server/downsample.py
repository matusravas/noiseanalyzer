# from scipy.io import wavfile
# from os import listdir, remove
# from os.path import isdir, isfile, join, exists
# import warnings
# import numpy as np
# import librosa
# warnings.filterwarnings("error")

# file = 'rii\\record.wav'

# # sr, data = wavfile.read(file)
# data, sr = librosa.load(file, sr=22050) # downsample by half to get nice spectrogram
# new_data = []
# for idx in range(0, len(data), 2):
#     new_data.append(data[idx])

# wavfile.write('down.wav', 11025, np.array(new_data))

import scipy.io.wavfile as wav

sr, data = wav.read('16bit_256len_65count_4096buffer32\\record.wav')

wav.write('16bit_256len_65count_4096buffer32\\record_amplifiedby16.wav',sr, data*16)