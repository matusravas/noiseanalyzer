import wave
from os import listdir
from os.path import isfile, join
# path = 'driller\\level_3\\'
path = 'trtr\\'
files = [f for f in listdir(path) if isfile(join(path, f)) and not f.endswith('.csv') and not f.endswith('.rar') and not f.startswith('record')]

def __sort_by(item):
    return int(item.split('_')[1].split('.')[0])

files.sort(key=__sort_by)
# print(files)

outfile = "record.wav"

data= []
for infile in files:
    w = wave.open(f'{path}{infile}', 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
    
output = wave.open(f'{path}{outfile}', 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()