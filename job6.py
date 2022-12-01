import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PIL import Image
from keras.models import load_model
import numpy as np
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
import pickle
import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17.0.5\bin\server'
form_window = uic.loadUiType('./UI/program.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ssg.com')
        self.setFixedSize(QSize(830, 650))
        self.model = load_model('./models/news_category_classification_model___96_9.h5')
        self.btn_check.clicked.connect(self.predict_review)
        self.initUI()
    def initUI(self):
        # self.setWindowTitle("My First Application")
        self.move(300,300)
        self.resize(400,200)
        self.show()
    def predict_review (self):
        X = self.txt_review.toPlainText()
        Y = ['kids']
        # print(1)

        with open('models/label_encoder.pickle', 'rb') as f:
            encoder = pickle.load(f)
        labeled_Y = encoder.transform(Y)
        onehot_Y = to_categorical(labeled_Y)
        # print(2)

        okt = Okt()
        X = okt.morphs(X, stem=True)
        # print(3)

        words=[]
        stopwords = pd.read_csv('stopwords.csv', index_col=0)
        for i in range(len(X)):
            if len(X[i]) > 1:
                if X[i] not in list(stopwords['stopword']):
                    words.append(X[i])
        X = ' '.join(words)
        print(X)

        token = Tokenizer()
        token.fit_on_texts(X)
        tokened_X = token.texts_to_sequences(X)
        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 88:
                tokened_X[i] = tokened_X[i][:88]
        # print(4)

        X_pad = pad_sequences(tokened_X, 88)

        model = load_model('./models/news_category_classification_model___96_9.h5')
        preds = model.predict(X_pad)
        # print(preds.shape)
        # print(preds[0].shape)
        # print(np.sum(preds[0]))
        label = encoder.classes_
        print(label)
        print(preds[0])
        print(np.argmax(preds[0]))
        category_pred = label[np.argmax(preds[0])]

        self.lbl_result.setText("해당 댓글은 {} 카테고리의 댓글입니다.".format(category_pred))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exam()
    sys.exit(app.exec_())