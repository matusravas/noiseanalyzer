import os
import socket
import time
import numpy as np
import io
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

categories = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6', 'level_7']

# Defining type of recieving bytes
dt = np.dtype(np.int16)
dt = dt.newbyteorder('<') #little endian

model_path = '..\\nn_models\\driller'

PORT = int(os.environ.get('PORT', '8082'))
if __name__ == '__main__':
    model = tf.keras.models.load_model(model_path)
    # model.summary()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind(('0.0.0.0', PORT))
    server.bind(('192.168.4.2', PORT))
    server.listen(5)
    size = 64  # 1024 #32768+44 number of bytes in one second of record +44 is header of wav
    print('Server listening on port: {}'.format(PORT))
    try:
        while True:
            client, addr = server.accept()
            start_conn = time.time()
            print('Accepted connection from: {}'.format(addr))
            client.settimeout(2)  # 2 by default
            buffer = io.BytesIO()
            try:
                cycles = 0
                while True:
                    data = client.recv(size)
                    cycles += 1
                    buffer.write(data)
                    if data == b'':
                        break
                # samples = np.frombuffer(buffer.getvalue(), dtype=dt, offset=44) # Reading bytes from bufer into numpy array
                start_pred = time.time()
                # samples = np.frombuffer(buffer.getvalue(), dtype=dt) # Reading bytes from bufer into numpy array
                # audio_binary = tf.io.read_file(file_path)
                audio, _ = tf.audio.decode_wav(buffer.getvalue(), desired_samples=22050)
                samples = tf.squeeze(audio, axis=-1)
                data = tf.cast(samples, tf.float32)
                spectrogram = tf.signal.stft(data, frame_length=255, frame_step=128)
                spectrogram = tf.abs(spectrogram)
                spectrogram = tf.expand_dims(spectrogram, -1)
                prediction = model(spectrogram) #predict
                prediction = np.argmax(prediction[0])
                category = categories[prediction]
                
                # fig, axes = plt.subplots(2, figsize=(12, 8))
                # timescale = np.arange(samples.shape[0])
                # axes[0].plot(timescale, samples.numpy())
                # axes[0].set_title('Waveform')
                # axes[0].set_xlim([0, 22050])
                # spec = spectrogram.numpy()
                # log_spec = np.log(spec.T)
                # height = log_spec.shape[0]
                # X = np.arange(22050, height)
                # Y = range(height)
                # axes[1].pcolormesh(log_spec)
                # axes[1].set_title('Spectrogram')
                # plt.show()
                
                
                # print('Transfer time: {}'.format(time.time() - start_conn))  # data transfer time
                # print('Prediction time: {}'.format(time.time() - start_pred))  # preprocesing/prediction time
                # print('Total time: {}'.format(time.time() - (start_conn + start_pred)))  # total time
                # print('Transfer speed: {}'.format(cycles*(size)/(time.time()-start_conn)))  # transfer speed
                
                print('Prediction: {}'.format(prediction))
                print('Category: {}'.format(category))
            except Exception as e:
                print('Timeout, closing socket...')
                print(type(e), str(e))
            buffer.close() # closing buffer
            client.close() # closing socket connection
            
    except KeyboardInterrupt:
        print('Exiting...')