import soundfile # to read audio file
import numpy as np
import librosa # to extract speech features
import glob
import os
import pickle # to save model after training
import pandas as pd

def extract_feature(file_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")

    if chroma or contrast:
        X, sample_rate = librosa.load(file_name)
        stft = np.abs(librosa.stft(X))
    result = np.array([])

    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
        result = np.hstack((result, mel))

    return result

def analyse(audio_path):
    
    # load the model from disk
    filename = "ada_classifier.model"
    loaded_model = pickle.load(open(filename, 'rb'))

    for file in glob.glob(audio_path):
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        
    ans = loaded_model.predict([features])
    return ans