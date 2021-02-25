from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import librosa
import numpy as np
from scipy.fftpack import fft
from scipy.signal import stft
from os import listdir
from os.path import isfile, join

pp = PdfPages('plots.pdf')
try:
    plots_printed = 0
    records = [f for f in listdir('./records') if isfile(join('./records', f)) and not f.endswith('.csv') and not f.startswith('record')]
    to_be_plotted = len(records)
    for record in records:
        if plots_printed == 0: # skipping first corupted/setup record from mic
            plots_printed += 1
            continue
        samples, sr = librosa.load(f'records/{record}')
        ffts = fft(samples)
        ffts = np.abs(ffts)
        ffts = ffts[:len(samples)//2]
        ffts = [2*freq/len(samples) for freq in ffts] 
        f, t, magnitude = stft(samples, fs=sr)
        
        fig, (ax1, ax2, ax3) = plt.subplots(3)
        ax1.plot(np.linspace(0,1, sr), samples, linewidth=.5)
        ax2.plot(ffts, linewidth=.5)
        ax3.pcolormesh(t, f, 20. * np.log10(np.abs(magnitude)))
        ax3.set_ylim([0,1000])
        # plt.show()
        pp.savefig(fig)
        plt.close(fig)
        plots_printed += 1
        if plots_printed%20 == 0:
            print(f'Printed {plots_printed}, remaining {to_be_plotted-plots_printed}')
    pp.close()
    
except Exception:  
    pp.close()
    
except KeyboardInterrupt:  
    pp.close()

