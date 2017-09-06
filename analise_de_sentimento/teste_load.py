#!/usr/bin/env python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np

from sklearn.externals import joblib


def load_model(filename):
    return joblib.load(filename)

def get_dataset(filename):
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), 'data', filename), 
        header=0, 
        delimiter="\t", \
        quoting=3 
    )

def clean_reviews(dataset):            
    cleaned_reviews = []
    for i in range(0, len(dataset["review"])):
        cleaned_reviews.append(
            " ".join(
                    KaggleWord2VecUtility.review_to_wordlist(
                        dataset["review"][i], True
        )))
    return cleaned_reviews


def create_bag_of_words(reviews):        
    vectorizer = CountVectorizer(analyzer = "word",   \
                            tokenizer = None,    \
                            preprocessor = None, \
                            stop_words = None,   \
                            max_features = 5000)    

    vectorizer = vectorizer.fit(reviews)
    data_features = vectorizer.transform(reviews)    
    return data_features

if __name__ == '__main__':        
    classifier = load_model('/home/eduardo/UEM/TCC/Git/TCC/analise_de_sentimento/nayve_kraggle.pkl')
    dataset = get_dataset('duh.tsv')        
    clean_reviews = clean_reviews(dataset)        
    predictions = classifier.predict(clean_reviews)
    output = pd.DataFrame(data={"id":dataset["id"], "sentiment":predictions} )            
    output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'predictions_loaded.csv'), index=False, quoting=3)        