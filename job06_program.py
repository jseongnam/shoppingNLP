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
from collections import Counter
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
        self.model = load_model('./models/reply_category_classification_model_0.753.h5')
        with open('models/label_encoder.pickle', 'rb') as f:
            self.encoder = pickle.load(f)
        with open('models/reply_token.pickle', 'rb') as f:
            self.token = pickle.load(f)
        self.label = self.encoder.classes_
        self.stopwords = pd.read_csv('stopwords.csv', index_col=0)
        self.btn_check.clicked.connect(self.predict_review)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My First Application")
        self.move(300,300)
        self.resize(400,200)
        self.show()

    def predict_review (self):
        X = self.txt_review.toPlainText()

        okt = Okt()
        X = okt.morphs(X, stem=True)
        # print(3)

        words=[]
        for i in range(len(X)):
            if len(X[i]) > 1:
                if X[i] not in list(self.stopwords['stopword']):
                    words.append(X[i])
        X = ' '.join(words)
        print(X)


        tokened_X = self.token.texts_to_sequences([X])
        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 88:
                tokened_X[i] = tokened_X[i][:88]
        print(tokened_X)

        X_pad = pad_sequences(tokened_X, 88)
        print(X_pad)

        preds = self.model.predict(X_pad)
        # print(preds.shape)
        # print(preds[0].shape)
        # print(np.sum(preds[0]))
        print(self.label)
        print(preds[0])
        print(np.argmax(preds[0]))
        category_pred = self.label[np.argmax(preds[0])]


        # for i in range(len(preds)):
        #     category_pred.append(np.argmax(preds[i]))
        # count_pre= Counter(category_pred)
        # category_pred = count_pred.most_common(n=1)


        self.lbl_result.setText("해당 댓글은 {} 카테고리의 댓글입니다.".format(category_pred))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exam()
    # mainWindow = Exam()
    # mainWindow.show()
    sys.exit(app.exec_())






        # try:
        # okt = Okt()
        # review = self.txt_review.toPlainText()
        # review = okt.morphs(review, stem=True)
        #
        # stopwords = pd.read_csv('./stopwords.csv', index_col=0)
        # words = []
        #
        # for i in range(len(review)):
        #     if len(review[i]) > 1:
        #         if review[i] not in list(stopwords['stopword']):
        #             words.append(review[i])
        # review = ' '.join(words)
        # print(review)
        #
        #
        # model = load_model('./models/reply_category_classification_model_0.735.h5')
        # print(1)
        # preds = model.predict(review)
        # print(2)
        # pred = np.argmax[preds]
        # print(pred)
        #
        # self.lbl_result.setText("해당 댓글은 {} 카테고리의 댓글입니다.".format(pred))
        #
        # except:
        #     self.lbl_result.setText("확인할 수 없습니다.")
        #







#
# if __name__ == "__main__":
#
#     app = QApplication(sys.argv)
#     mainWindow = Exam()
#     mainWindow.show()
#     sys.exit(app.exec_())
