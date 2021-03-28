from flask import Flask
from flask.globals import request
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()
app = Flask (__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet') #async_mode='threading'

clients = []

@socketio.on('connect')
def connect():
    print ('client connected')
    emit('data', {'msg': 'hi'})
    print(request.sid)
    clients.append(request.sid)

@socketio.on('disconnect')
def disconnect():
    print ('client disconnect')


def run_socket():
    import os
    import socket
    import time
    import numpy as np
    import io
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    import tensorflow as tf
    
    dt = np.dtype(np.int16)
    dt = dt.newbyteorder('<') #little endian

    model_path = 'nn_models\\engines'
    model = tf.keras.models.load_model(model_path)
    
    PORT = int(os.environ.get('PORT', '8082'))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    categories =['engine_fabia1_0', 'engine_fabia1_4', 'engine_golf', 'engine_octavia', 'engine_passat']


    
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    size = 64
    print('Server listening on port: {}'.format(PORT))
    timed_out = []
    idx = 0
    try:
        while True:
            client, addr = server.accept()
            print('Accepted connection from: {}'.format(addr))
            client.settimeout(2)  # 2 by default
            buffer = io.BytesIO()
            try:
                start = time.time()
                cycles = 0
                idx += 1
                while True:
                    data = client.recv(size)
                    cycles += 1
                    buffer.write(data)
                    if data == b'':
                        break
                start = time.time()
                record, _ = tf.audio.decode_wav(buffer.getvalue(), desired_samples=16000)
                samples = tf.squeeze(record, axis=-1)
                data = tf.cast(samples, tf.float32)
                spectrogram = tf.signal.stft(data, frame_length=1024, frame_step=512)
                spectrogram = tf.abs(spectrogram)
                spectrogram = tf.expand_dims(spectrogram, -1)
                prediction = model(spectrogram) #predict
                prediction = np.argmax(prediction[0])
                category = categories[prediction]
                print(category, prediction)
                print(time.time() - start)
                socketio.emit('data', {'prediction': f'{prediction}', 'label': f'{category}', 'samples': samples.numpy().tolist()})
            except Exception as e:
                socketio.emit('data', {'msg': f'hola {idx}'})
                print(type(e), e)
            client.close()
            
    except KeyboardInterrupt:
        print('Exit, Interrupted...')
        

if __name__ == '__main__':
    t = socketio.start_background_task(target=run_socket)
    socketio.run(app, port=8080)