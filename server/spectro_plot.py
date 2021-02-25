import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import stft

idx = 0
fig, ax = plt.subplots(2,3)
for i in range(0,2):
    for j in range(0,3):
        idx += 1
        level = f'level_{idx}'
        samples, sr = librosa.load(f'driller\\{level}\\audio_100.wav', sr=22050) # downsample by half to get nice spectrogram
        stf = librosa.stft(np.array(samples))
        f, t, magnitude = stft(samples, fs=sr)    
        ax[i][j].pcolormesh(t, f, 20. * np.log10(np.abs(magnitude)))
        ax[i][j].set_title(level)
plt.show()