import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

df=pd.read_csv('vendor.csv')

df['Vendor Name'] = df['Vendor Name'].str.lower()

x_train=df['Vendor Name'].tolist()
y_train=df['Vendor Code'].tolist()

tfdif=TfidfVectorizer()

train_vectors=tfdif.fit_transform(x_train)

svm = OneVsRestClassifier(SVC(kernel='linear', gamma='scale', probability=True))
svm.fit(train_vectors, y_train)

def vendor_model(vendor_names):
    vendor_names_vector=tfdif.transform(vendor_names)
    test_probabilities = svm.predict_proba(vendor_names_vector)
    anomaly_scores = [1 - max(probs) for probs in test_probabilities]
    l=[]
    j=0
    for i in anomaly_scores:
        if i>0.87:
            output='-1'
        else:
            output=list(svm.predict(vendor_names_vector[j]))
            output=str(output[0])
        j=j+1
        l.append(output)       
    return l