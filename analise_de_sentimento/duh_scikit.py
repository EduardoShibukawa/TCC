#!/usr/bin/env python

import os
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

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
    classificador = MultinomialNB()        
    classificador = classificador.fit(data_features, data_labels)
    return classificador        

def save_dataset(dataset, predictions):
    output = pd.DataFrame(data={"data":dataset['data'],"titulo":dataset["titulo"], "sentimento":predictions})            
    output.to_csv(
        os.path.join(os.path.dirname(__file__), '..//data', 'scikit_sentimentos.csv')    
    )    

def generate_csv(classifier, dataset, data_features):
    predictions = classifier.predict(data_features)        
    save_dataset(dataset, predictions)    

def cross_validation(classifier_name, classifier, X, y):
    # Applying k-Fold Cross Validation
    from sklearn.model_selection import cross_val_score
    accuracies = cross_val_score(estimator = classifier, X = X, y = y, cv = 10)    
    print(classifier_name)
    print("------------------------")
    print("Accuracias dos Folds: {}".format(accuracies))
    print("Media Accuracia: {}".format(accuracies.mean()))
    print("Std: {}".format(accuracies.std()))
    print("------------------------")

    
def gerar_metricas(classifier_name, y_true, y_pred):        
    import sklearn.metrics as skm        
    # Making the Confusion Matrix
    cm = skm.confusion_matrix(y_true, y_pred)        
    np.set_printoptions(precision=2)
    
    # Plot non-normalized confusion matrix
    class_names =['Negativo', 'Neutro', 'Positivo']    
    plot_confusion_matrix(cm, classes=class_names,
                          title='Matriz de confusão de setembro')
    plt.savefig('..//data//cm_{}.png'.format(classifier_name))        
    
    # Plot normalized confusion matrix        
    """
    np.set_printoptions(precision=2)
    plot_confusion_matrix(cm, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')        
    np.set_printoptions(precision=2)
    plt.savefig('..//data//cm_{}_normal.png'.format(classifier_name))
    """
    
    precision, recall, fbeta_score, support = skm.precision_recall_fscore_support(y_true, y_pred, average='macro')    
    print("Kappa: {}".format(skm.cohen_kappa_score(y_true,y_pred)))    
    print("Precisão: {}".format(precision))
    print("Recall: {}".format(recall))   
    print("FBeta: {}".format(fbeta_score))
    print("Suporte: {}".format(support))        
    print("----------------------------")    
    
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):    
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]        
    
    thresh = cm.max() / 2.  
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')    

def testar(classificador, X,Y):    
    y_pred = classificador.predict(X)    
    gerar_metricas('Nayve', Y, y_pred)                        

dataset_train = pd.concat([        
        get_dataset_g1_treino('noticias_maio.csv'),
        get_dataset_g1_treino('noticias_junho.csv'),
        get_dataset_g1_treino('noticias_julho.csv'),
        get_dataset_g1_treino('noticias_agosto.csv'),                
        get_dataset_g1_treino('noticias_setembro.csv'),
    ], ignore_index=True 
)

dataset_test = pd.concat([                
        get_dataset_g1_treino('noticias_outubro.csv'),      
    ], ignore_index=True 
)

print("Limpando textos")
train = clean_text_field(dataset_train, 'conteudo', False)
test = clean_text_field(dataset_test, 'conteudo', False)

print("Criando bag of words")
from sklearn.model_selection import train_test_split
feature_train, feature_test, _ = create_bag_of_words(train, test)
X_train, X_test, y_train, y_test = train_test_split(feature_train, dataset_train['sentimento'], test_size = 0.2, random_state=1000)

print("Treinando classificador")
nayve_classifier = train_nayve(X_train, y_train)

print("Cross validation")
cross_validation('Nayve', nayve_classifier, X_train, y_train)

print("Testando dataset de treino")
testar(nayve_classifier, X_test, y_test)

print("Testando dataset de teste real")
testar(nayve_classifier, feature_test, dataset_test['sentimento'])

print("Gerando CSV")
generate_csv(nayve_classifier, dataset_test, feature_test)

print("Finalizado")