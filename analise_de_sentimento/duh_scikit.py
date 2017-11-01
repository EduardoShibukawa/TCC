#!/usr/bin/env python

import os
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np

def get_dataset_g1_treino(filename):
    dataset = pd.read_csv(
      os.path.join(os.path.dirname(__file__), '..//data', filename),
      usecols= ['data_atualizacao', 'titulo', 'conteudo', 'sentimento']        
    )        
    dataset.rename(columns={'data_atualizacao': 'data'}, inplace=True)    

    return dataset    

def get_dataset_g1(filename):    
    dataset = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..//data', filename), 
        usecols= ['data_atualizacao', 'titulo', 'conteudo']                
    )    
    dataset.rename(columns={'data_atualizacao': 'data'}, inplace=True)

    return dataset

def clean_text_field(dataset, fieldname, translate):
    cleaned_field = []
    for i in range(0, len(dataset[fieldname])):
        if translate:            
            blob = TextBlob(dataset[fieldname][i]).translate(from_lang='pt-br', to="en")            
            cleaned_field.append(
                " ".join(
                        KaggleWord2VecUtility.review_to_wordlist(
                            str(blob), True
            )))
        else :
            cleaned_field.append(
                    " ".join(
                            KaggleWord2VecUtility.review_to_wordlist(
                                dataset[fieldname][i], True
                )))
    return cleaned_field


def create_bag_of_words(train_data, test_data):    
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)    
    data_features_train = vectorizer.fit_transform(train_data)
    data_features_test = vectorizer.transform(test_data)    
    return data_features_train, data_features_test, vectorizer

def train_nayve(data_features, data_labels):
    from sklearn.naive_bayes import MultinomialNB

    nayve = MultinomialNB()
    nayve = nayve.fit(data_features, data_labels)
    return nayve

def save_dataset(dataset, predictions):
    output = pd.DataFrame(data={"data":dataset['data'],"titulo":dataset["titulo"], "sentimento":predictions})            
    output.to_csv(
        os.path.join(os.path.dirname(__file__), '..//data', 'scikit_sentimentos.csv')    
    )    

def generate_csv(classifier, dataset, data_features):
    predictions = classifier.predict(data_features)        
    save_dataset(dataset, predictions)    
    

dataset_train = get_dataset_g1_treino('g1_noticias_treino.csv')
dataset_test = get_dataset_g1('noticias_teste.csv')

print("Limpando textos")
train = clean_text_field(dataset_train, 'conteudo', False)
test = clean_text_field(dataset_test, 'conteudo', True)

print("Criando bag of words")
feature_train, feature_test, _ = create_bag_of_words(train, test)

print("Criando e treinando dados")
nayve_classifier = train_nayve(feature_train, dataset_train["sentimento"])

print("Gerando CSV")
generate_csv(nayve_classifier, dataset_test, feature_test)

print("Finalizado")