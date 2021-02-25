# from pydub import AudioSegment
import librosa
import os
import scipy.io.wavfile as wav
sr = 44100
start = 0
end = sr
idx = 0

samples, sr = librosa.load('rii\\Recording_5.wav', sr=sr)

path = 'splits\\'
if not os.path.exists(path):
     os.makedirs(path)

while end < len(samples):
    data = samples[start:end]
    start = end
    end += sr 
    wav.write(f'{path}audio_{idx}.wav', sr, data)
    idx += 1