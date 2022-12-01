from keras.models import *
from keras.layers import *
import numpy as np
from keras.callbacks import EarlyStopping

X_train, X_test, Y_train, Y_test = np.load(
    './models/reply_data_max_88_wordsize_9835.npy', allow_pickle = True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

early_stopping = EarlyStopping(patience = 3)
my_dict = {} # evaluate 값 저장 dict
for i in range(10): # batch_size 32배수로 training
    for j in range(5): # kernel_size 바꾸면서 training
        model = Sequential()
        model.add(Embedding(21001, 300, input_length = 88))           # Embedding 안에는 wordsize 값.
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
