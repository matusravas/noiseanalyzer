from scipy.io import wavfile
from os import listdir, remove
from os.path import isdir, isfile, join, exists
import warnings
import numpy as np
import librosa
warnings.filterwarnings("error")

folder = 'test\\'
files = [join(folder, path) for path in listdir(folder) if isfile(join(folder, path))]

num_of_removed = 0
removed_files = []

def remove_corrupted(file, num_of_removed, removed_files):
    # print(file)
    num_of_removed += 1
    removed_files.append(file)
    # remove(file)

def __sort_by(item):
    # print(item)
    return int(item.split('\\')[1].split('_')[1].split('.')[0])

files.sort(key=__sort_by)
for file in files:
    try:
        # sr, data = wavfile.read(file)
        data, sr = librosa.load(file, sr=16000) # downsample by half to get nice spectrogram
        # if len(data) < 44100:
        #     remove_corrupted(file, num_of_removed, removed_files)
        for idx in range(16, len(data), 16):
            res = 0
            for i in range(0,16):
                res += np.abs(data[idx-i])
            if res == 0:
                # print(idx)
                remove_corrupted(file, num_of_removed, removed_files)
                break
        # if np.any(data[:] == 0):
            # remove_corrupted(file, num_of_removed, removed_files)
    except ValueError:
        remove_corrupted(file, num_of_removed, removed_files)
    except wavfile.WavFileWarning:
        remove_corrupted(file, num_of_removed, removed_files)

print(f'corrupted: {num_of_removed}')
for rmf in removed_files:
    print(rmf)