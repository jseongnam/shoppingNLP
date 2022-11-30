import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './reply_data_max_88_wordsize_11859.npy', allow_pickle = True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# from konlpy.tag import Okt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import pickle
from keras.models import load_model
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(patience = 3)
my_dict = {}
for i in range(10):
    for j in range(5):
        model = Sequential()
        model.add(Embedding(28050, 300, input_length = 88))           # Embedding 안에는 wordsize 값.
        model.add(Conv1D(64, kernel_size = 7+j, padding='same', activation='relu'))
        model.add(MaxPool1D(pool_size = 1))
        model.add(GRU(128, activation='tanh', return_sequences=True))
        # return_sequences :  1) True = GRU 1회를 돌려 받은 값들을 시퀀스 형태로 저장. 2) False = GRU를 돌려 나온 마지막 값을 저장.
        model.add(Dropout(0.3))
        model.add(GRU(64, activation='tanh', return_sequences=True))
        model.add(Dropout(0.3))
        model.add(GRU(64, activation = 'tanh'))
        model.add(Dropout(0.3))
        model.add(Flatten())
        model.add(Dense(128, activation="relu"))
        model.add(Dense(7, activation='softmax'))
        model.summary()

        model.compile(loss='categorical_crossentropy', optimizer='adam',
                    metrics=['accuracy'])
        fit_hist = model.fit(X_train, Y_train, batch_size=32*(i+1),
                            epochs=20, validation_data=(X_test, Y_test),callbacks = [early_stopping])
        model.save('./models/news_category_classification_model___{}_{}.h5'.format(32*(i+1),7+j))
        my_dict['batch_size = {}, kernel_size = {}'.format(32*(i+1),7+j)] =model.evaluate(X_test,Y_test)[1]
    # plt.plot(fit_hist.history['accuracy'], label = 'accuracy')
    # plt.plot(fit_hist.history['val_accuracy'], label = 'val_accuracy')
    # plt.legend()
    # plt.show()