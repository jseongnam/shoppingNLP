import pandas as pd
import numpy as np
from konlpy.tag import Okt
from keras_preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import pickle
from keras.models import load_model
import zipfile
import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17.0.5\bin\server'
print('JAVA_HOME' in os.environ)
# zipfile.ZipFile('./models/news_category_classification_model___96_9.zip').extractall('./models')
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)
df = pd.read_csv('./crawling_data_2/crawling_data.csv')
print(df.head())
df.info()


X = df['reply']
Y = df['category']

with open('./models/label_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_Y)

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./stopwords.csv', index_col = 0)
for j in range (len(X)):
    words = []
    for i in range (len(X[j])):
        if len(X[i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
              words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/reply_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
for i in range (len(tokened_X)):
    if len(tokened_X[i]) > 88:
        tokened_X[i] = tokened_X[i][:88]

X_pad = pad_sequences(tokened_X, 88)


model = load_model('./models/reply_category_classification_model_0.753.h5')
preds = model.predict(X_pad)
label = encoder.classes_
category_preds = []
for pred in preds:
    category_pred = label[np.argmax(pred)]
    category_preds.append(category_pred)
df['predict'] = category_preds



df['OX'] = False
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = True


print(df.head(30))
print(df['OX'].value_counts())
print(df['OX'].mean())
print(df.loc[df['OX']==False])
print('debug01')