import librosa
from librosa.display import specshow
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, rfft, fftfreq
from scipy.signal import stft
from scipy.io import wavfile as wav

import time

start = time.time()
# samples0, sr = librosa.load(f'./datasets/rooms_white_noise/my_bedroom/audio_126.wav', sr=16000)
# samples0, sr = librosa.load('16bit_256len_65count_4096buffer32/record_amplifiedby16.wav', sr=16000) # downsample by half to get nice spectrogram
# samples0, sr = librosa.load('Recording_3.wav', sr=16000) # downsample by half to get nice spectrogram
# samples0, sr = librosa.load('record_mirroring.wav', sr=22050) # downsample by half to get nice spectrogram
samples0, sr = librosa.load('trtr/cat1/audio_0.wav', sr=16000)
# samples0, sr = librosa.load('mini_speech_commands\\right\\0ab3b47d_nohash_0.wav', sr=22050)
# samples0 = samples0[:sr]
# wav.write("e.wav", sr, np.array(samples0))

# np.savetxt('data.txt', samples0)
    
# with open('data.txt', 'w') as f:
#     f.write(str(samples0))
# s = np.abs(librosa.stft(samples0))
# fig, ax = plt.subplots()
# img =specshow(librosa.amplitude_to_db(s,ref=np.max), y_axis='log', x_axis='time', ax=ax)
# ax.set_title('Power spectrogram')
# fig.colorbar(img, ax=ax, format="%+2.0f dB")

print(sr, len(samples0))
samples = []
n = 1
# r = range(n, len(samples0))
start_filter = time.time()
for i in range(n):
    samples.append(samples0[i])
for i in range(n, len(samples0)):
    a = 0
    for j in range(n):
        a += samples0[i-j]
    a = a/n
    samples.append(a)
# print(time.time() - start_filter)

# from scipy.io.wavfile import write
# t = np.linspace(0., 1., sr)
# write("example.wav", sr, np.array(samples))

# print(len(samples), sr)
start_fft = time.time()
ffts = fft(samples)
ffts = np.abs(ffts)
ffts = ffts[:len(samples)//2]
ffts = [2*f/len(samples) for f in ffts] 

# ffts = -20. * np.log10(ffts)
# freqs = freqs[:1000]
# print(time.time() - start_fft) #0.0546870231628418
start_stft = time.time()
stf = librosa.stft(np.array(samples))
f, t, magnitude = stft(samples, fs=sr, nperseg=1024, noverlap=512)
# print(time.time() - start_stft)
# print(time.time() - start)

# magnitude2 = []
# for i in range(len(f[:65])):
#     magnitude2.append(magnitude[:65])
#     # magnitude[i] = magnitude[i][:150]
# mag = np.array(magnitude2)
# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(np.linspace(0, 1, len(samples)), samples, linewidth=.1)
# ax2.plot(ffts, linewidth=.1)
# ax3.pcolormesh(t, f, 20. * np.log10(np.abs(magnitude)))
plt.plot(ffts, linewidth=.5)
plt.show()
plt.pcolormesh(t, f, 20. * np.log10(np.abs(magnitude)))
plt.show()