import sys
import numpy as np
import re
import json
from Stemmer import Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

# "Stemmer" służy do redukcji słów do ich rdzenia.
def text_cleaner(text, language):
    stemmer = Stemmer(language)
    text = text.lower() # zmiana do lowerCase
    text = ' '.join( stemmer.stemWords( text.split() ) ) 
    text = re.sub( r'\b\d+\b', ' digit ', text ) # zamiana liczb
    return  text 

# wgrywanie danych z pliku model.txt

with open("model.txt", "r") as f:
    lines = f.readlines()
    data = []
    for line in lines:
        if line.startswith("#"):
            continue
        text, tag = line.split("@")[:2]
        data.append({"text": text, "tag": tag})
    json_data = json.dumps(data)

with open("model.json", "w") as f:
    f.write(json_data)

# Nauka 

def train_test_split(data, validation_split = 0.2):
    if not(0 <= validation_split <= 1):
        raise ValueError("validation_split must be between 0 and 1 (inclusive)")
    sz = len(data)
    indices = np.arange(sz)
    np.random.shuffle(indices)

    X = [data[i]['text'] for i in indices]
    Y = [data[i]['tag'] for i in indices]
    nb_validation_samples = int( validation_split * sz )

    return { 
        'train': {'x': X[:-nb_validation_samples], 'y': Y[:-nb_validation_samples]},
        'test': {'x': X[-nb_validation_samples:], 'y': Y[-nb_validation_samples:]}
    }



def openai():
    with open("model.json", "r") as f:
        json_data = f.read()
    data = json.loads(json_data)
    D = train_test_split(data)
    text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                         ('clf', SGDClassifier(loss='log')),
                         ])
    text_clf.fit(D['train']['x'], D['train']['y'])
    accuracy = text_clf.score(D['test']['x'], D['test']['y'])
    print(f"Accuracy on test set: {accuracy:.2f}")

    text_clf.fit(D['train']['x'], D['train']['y'])
    predicted = text_clf.predict( D['train']['x'] )
    predictions = text_clf.predict(D['test']['x'])

    from sklearn.metrics import classification_report
    
   

    print(classification_report(D['test']['y'], predictions))
       
    z = input("Wprowadz swoje pytanie bez znaku zapytania na koncu: ")
    zz = []
    zz.append(z)
    predicted = text_clf.predict(zz) 
    print(predicted[0])

if __name__ == '__main__':
    sys.exit(openai())