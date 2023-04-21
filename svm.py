import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


df=pd.read_csv('data.csv')

japanese_stop_words = ['あの', 'いくつか', 'いつ', 'そして', 'その', 'たくさん', 'だから', 'とても', 'どうして', 'なぜ']
arabic_stop_words = ['أنا', 'هو', 'في', 'من', 'على', 'إلى', 'هذا', 'الذي', 'الذين', 'إذا']

sw=["au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en", "et", "eux", "il", "je", "la", "le", "leur", "lui", "ma", "mais", "me", "même", "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on", "ou", "par", "pas", "pour", "qu", "que", "qui", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "toi", "ton", "tu", "un", "une", "vos", "votre", "vous"
]+list(ENGLISH_STOP_WORDS)+japanese_stop_words+arabic_stop_words

for i in df.index:
    cc=df.loc[i,'Cost Center']
    gla=df.loc[i,'GL Account']
    df.loc[i,"ylabel"]=str(cc)+","+str(gla)

df['Description '] = df['Description '].str.lower()

x_train=df['Description '].tolist()

y_train=df['ylabel'].tolist()

tfdif=TfidfVectorizer(stop_words=sw)

train_vectors=tfdif.fit_transform(x_train)

svm = OneVsRestClassifier(SVC(kernel='linear', probability=True))
svm.fit(train_vectors, y_train)


def svmmodel(description):
    description_vector=tfdif.transform(description)
    test_probabilities = svm.predict_proba(description_vector)
    anomaly_scores = [1 - max(probs) for probs in test_probabilities]
    l=[]
    j=0
    for i in anomaly_scores:
        if i>0.78:
            output=[-1,-1]
        else:
            output=list(svm.predict(description_vector[j]))
            output=list(output[0].split(','))
        j=j+1
        l.append(output)       
    return l