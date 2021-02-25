import os
import socket
import time
import csv
import numpy as np
import scipy.io.wavfile as wav
import io
import asyncio

PORT = int(os.environ.get('PORT', '8082'))
# category = 'level_7'
# dataset_name = 'driller'
# path = '{}\\{}\\'.format(dataset_name, category)
path = 'test\\'

def save_timeouts():
    if timed_out:
        with open(f'{path}timeouts.csv', 'w', newline='') as f: #for simple recording
            writer = csv.writer(f)
            for e in timed_out:
                writer.writerow(["{}".format(e.split('\\')[1])])


if __name__ == '__main__':
    if not os.path.exists(path):
        os.makedirs(path)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Defining type of recieving bytes
    dt = np.dtype(np.int16)
    dt = dt.newbyteorder('<') #little endian
    
    server.bind(('0.0.0.0', PORT))
    # server.bind(('192.168.4.2', PORT))
    server.listen(5)
    size = 64  # 1024 #32768+44 number of bytes in one second of record +44 is header of wav
    idx = 0
    print('Server listening on port: {}'.format(PORT))
    timed_out = []
    try:
        while True:
            client, addr = server.accept()
            print('Accepted connection from: {}'.format(addr))
            client.settimeout(2)  # 2 by default
            f = open('{}audio_{}.wav'.format(path, idx), 'wb')
            idx += 1
            buffer = io.BytesIO()
            try:
                start = time.time()
                cycles = 0
                while True:
                    data = client.recv(size)
                    cycles += 1
                    buffer.write(data)
                    if data == b'':
                        break
                    f.write(bytearray(data)) # independant operation, maybe in another PC thread
                
                bytes_ = np.frombuffer(buffer.getvalue(), dtype=dt)
                # with open('{}audio_{}.txt'.format(path, idx), 'wb') as bf:
                #     bf.write(buffer.getvalue())
                # wav.write(,sr,)
                # print(time.time()-start)  # data transfer time
                # print(cycles*(size)/(time.time()-start))  # transfer speed
            except Exception as e:
                timed_out.append('audio_{}.wav'.format(idx))
                print(type(e))
            f.close() # closing file
            client.close() # closing socket connection
            if idx >= 550:
                save_timeouts()
                print('Exit, OK...')
                exit()
            
    except KeyboardInterrupt:
        save_timeouts()
        print('Exit, Interrupted...')
        
