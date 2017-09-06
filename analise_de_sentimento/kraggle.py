#!/usr/bin/env python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np

from sklearn.externals import joblib

def save_model(classifier, filename):    
    joblib.dump(classifier, filename) 


def load_model(filename):
    return joblib.load(filename)


def get_dataset(filename):
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), 'data', filename), 
        header=0, 
        delimiter="\t", \
        quoting=3 
    )


def save_dataset(dataset, predictions):
    output = pd.DataFrame(data={"id":dataset["id"], "sentiment":predictions} )            
    output.to_csv(
        os.path.join(os.path.dirname(__file__), 'data', 'predictions.csv'), 
        index=False, quoting=3
    )    

def generate_csv(classifier, dataset, data_features):
    predictions = classifier.predict(data_features)        
    save_dataset(dataset, predictions)    
    

def clean_reviews(dataset):            
    cleaned_reviews = []
    for i in range(0, len(dataset["review"])):
        cleaned_reviews.append(
            " ".join(
                    KaggleWord2VecUtility.review_to_wordlist(
                        dataset["review"][i], True
        )))
    return cleaned_reviews


def create_bag_of_words(train_reviews, test_reviews):    
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)    

    data_features_train = vectorizer.fit_transform(train_reviews)
    data_features_test = vectorizer.transform(test_reviews)    
    return data_features_train, data_features_test, vectorizer

def train_nayve(data_features, data_labels):
    from sklearn.naive_bayes import MultinomialNB


    nayve = MultinomialNB()
    nayve = nayve.fit(data_features, data_labels)
    return nayve

def train_random_forest(data_features, data_labels):
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(data_features, data_labels)
    return forest

def summarize_labeled(classifier, data_features, data_labels):    
    from sklearn import metrics
    
    predictions = classifier.predict(data_features)
    predictions_probs = classifier.predict_proba(data_features)
    accuracy = classifier.score(data_features, data_labels)    
    precision, recall, f1, _ =  metrics.precision_recall_fscore_support(
        data_labels, predictions
    )

    print("")
    print("Accuracy = ", accuracy)
    print("Precision = ", precision)
    print("Recall = ", recall)
    print("F1 Score = ", f1)

def create_pipeline(vector, classifier):
    from sklearn.pipeline import Pipeline

    
    return pipeline = Pipeline([
        ('vect', vector),        
        ('clf', classifier),
    ])


if __name__ == '__main__':    
    print("Abrindo dados do arquivos")
    train =  get_dataset('labeledTrainData.tsv')
    test = get_dataset('testData.tsv')

    print("Limpando texto dos arquivos")            
    clean_reviews_train = clean_reviews(train)                        
    clean_reviews_test = clean_reviews(test)

    print("Criando bag of words")
    data_features_train, data_features_test, vectorizer = create_bag_of_words(clean_reviews_train, clean_reviews_test)     

    print("Treinando classificador")
    nayve_classifier = train_nayve(data_features_train, train["sentiment"])
    #forest_classifier = train_random_forest(data_features_train, train["sentiment"])

    print("Testando classificador")
    print("Gerando arquivo com resultados das predições")    
    generate_csv(nayve_classifier, test, data_features_test)
    #generate_csv(forest_classifier, test, data_features_test)    

    save_model(nayve_classifier, 'nayve_kraggle.pkl')    
    #save_model(forest_classifier, 'forest_kraggle.pkl')
    #summarize_labeled(train, train["sentiment"])

    pipeline = create_pipeline(vectorizer, nayve_classifier)        
    predicted = pipeline.fit_transform(Xtrain).predict(Xtrain)
    # Now evaluate all steps on test set
    predicted = pipeline.predict(Xtest)