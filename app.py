from flask import Flask, jsonify, render_template, request
import tensorflow as tf
from tensorflow.keras.models import load_model
import python_speech_features
import numpy as np
# import base64
from pydub import AudioSegment
# import io
from werkzeug.utils import secure_filename
import os
from scipy.io import wavfile

# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession
# config = ConfigProto()
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

app = Flask(__name__)

# word2index = {
#     # core words
#     "yes": 0,
#     "no": 1,
#     "up": 2,
#     "down": 3,
#     "left": 4,
#     "right": 5,
#     "on": 6,
#     "off": 7,
#     "stop": 8,
#     "go": 9,
#     "zero": 10,
#     "one": 11,
#     "two": 12,
#     "three": 13,
#     "four": 14,
#     "five": 15,
#     "six": 16,
#     "seven": 17,
#     "eight": 18,
#     "nine": 19,
# }
# index2word = [word for word in word2index]

word2index = {
    # core words
    "cancel": 0,
    "digit": 1,
    "direction": 2,
    "down": 3,
    "left": 4,
    "right": 5,
    "options": 6,
    "open": 7,
    "yes": 8,
    "no": 9,
    "zero": 10,
    "one": 11,
    "two": 12,
    "three": 13,
    "four": 14,
    "five": 15,
    "six": 16,
    "seven": 17,
    "eight": 18,
    "nine": 19,
}
index2word = [word for word in word2index]

def extract_loudest_section(audio, length):
    audio_pw = audio**2 # power
    window = np.ones((length, ))
    conv = np.convolve(audio_pw, window, mode="valid")
    begin_index = conv.argmax()
    return audio[begin_index:begin_index+length]

def get_model():
    global model
    model = load_model("models\\05_04_2022__17_38_arab.h5")
    print("Model loaded")

def preprocess_audio(audio):
    audio = audio.astype(np.float)
    # normalize data
    audio=audio.astype('float32')
    audio -= audio.mean()
    audio /= np.max((audio.max(), -audio.min()))
    # compute MFCC coefficients
    features = python_speech_features.mfcc(audio, samplerate=16000, winlen=0.025, winstep=0.01, numcep=20, nfilt=40, nfft=512, lowfreq=100, highfreq=None, preemph=0.97, ceplifter=22, appendEnergy=True, winfunc=np.hamming)
    return features

get_model()

UPLOAD_FOLDER = "uploads"

@app.route("/upload")
#somecode

@app.route("/predict", methods=["POST"])
def predict():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # message = request.get_json(force=True)
    # encoded = message['audio']
    # decoded = base64.b64decode(encoded)
    # audio = AudioSegment.from_file(io.BytesIO(decoded), format="wav")
    # print(audio)
    #preprocess

    # samples = audio.get_array_of_samples()
    # samples = np.array(samples)

    samplerate, data = wavfile.read(filepath)
    recording = extract_loudest_section(data, int(1*16000))
    audio_preprocessed = preprocess_audio(recording)
    recorded_feature = np.expand_dims(audio_preprocessed, 0)
    prediction = model.predict(recorded_feature).reshape((20, ))
    prediction /= prediction.sum()
    #=======================================================
    prediction_sorted_indices = prediction.argsort()

    label = []
    percentage = []
    for k in range(3):
        i = int(prediction_sorted_indices[-1-k])
        label.append(index2word[i])
        percentage.append(prediction[i]*100)
        print("%d.)\t%s\t:\t%2.1f%%" % (k+1, label[k], percentage[k]))
    
    response = {
        'prediction' : {
            'label1' : label[0],
            'prob1' : percentage[0],
            'label2' : label[1],
            'prob2' : percentage[1],
            'label3' : label[2],
            'prob3' : percentage[2]
        }
    }
    #=======================================================
    # response = {
    #     "prediction" : prediction
    # }

    return jsonify(response)

@app.route("/home")
def home():
    return render_template("home.html")

# if __name__ == '__main__':
#     # This is used when running locally only. When deploying to Google App
#     # Engine, a webserver process such as Gunicorn will serve the app.
#     app.run(host='127.0.0.1', port=8080, debug=True)
# # [END gae_flex_quickstart]