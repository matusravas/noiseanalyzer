from os import listdir, remove
from os.path import isdir, isfile, join, exists
# wav = 'audio_0.wav'
folder = '.\\records'
category_folders = [join(folder, path) for path in listdir(folder) if isdir(join(folder, path))]

for path in category_folders:
    files = [join(path, file) for file in listdir(path)]
    last_10 = files[-10:]
    first_10 = files[:10]
    for file in first_10:
        if exists(file) and isfile(file):
            # print(file)
            remove(file)
    for file in last_10:
        if exists(file) and isfile(file):
            # print(file)
            remove(file)
