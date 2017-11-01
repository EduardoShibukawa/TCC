from registro01 import Registro01
import peewee

import os
import pandas as pd
import numpy as np

from scipy.stats.stats import pearsonr

import re
from datetime import datetime, timedelta

def save_dictionary(dictionary, name):
    np.save(
        os.path.join(os.path.dirname(__file__), '..//data', name), 
        dictionary
    ) 

def get_dataset(filename):
    try:
        return pd.read_csv(
            os.path.join(os.path.dirname(__file__), '..//data', filename),
            usecols=['data', 'sentimento']
        )             
    except:
        dataset =  pd.read_csv(
            os.path.join(os.path.dirname(__file__), '..//data', filename),
            usecols=['data_atualizacao', 'sentimento']
        )     
        dataset.rename(columns={'data_atualizacao': 'data'}, inplace=True)    
        return dataset

def get_acao_petrobras(data_pregao):  
    try:
        return Registro01 \
                    .select() \
                        .where(Registro01.codigo_negociacao.endswith('PETR4') \
                                & (Registro01.data_pregao.startswith(data_pregao))).get()
    except:
        return None        

def get_correlacao(x, y):
    return pearsonr(y, x)

def normalizar_sentimentos(sentimentos):
    sentimentos_dup = sentimentos.copy()
    for key in sentimentos_dup.keys():
        if sentimentos_dup[key] > 1:
            sentimentos_dup[key] = 1
        elif sentimentos_dup[key] < -1:
            sentimentos_dup[key] = -1                                

    return sentimentos_dup

def gerar_valores_e_sentimentos(dataset):
    regex = r"(\d{2})\/(\d{2})\/(\d{4})"
    subst = r"\3\2\1"

    sentimentos = {}
    valores_acao = {}
    for index, row in dataset.iterrows():        
        data = re.sub(regex, subst, row['data'], 0)            
        data = data.strip()        
        data = datetime.strptime(data, "%Y%m%d").date() + timedelta(days=0)
        acao = get_acao_petrobras(data.strftime('%Y%m%d'))        
        if data not in sentimentos:
            sentimentos[data] = row['sentimento']        
        else:
            sentimentos[data] += row['sentimento']
        
        if (acao and data not in valores_acao):
            valores_acao[data] = float(acao.preco_ultimo)    

    return valores_acao, sentimentos


def gerar_correlacao(dataset):
    valores_acao, sentimentos = gerar_valores_e_sentimentos(dataset)

    sentimentos_sem_acao = {key: sentimentos[key] for key in sentimentos if key not in list(valores_acao.keys())}    
    sentimentos = {key: sentimentos[key] for key in sentimentos if key not in list(sentimentos_sem_acao.keys())}    
    
    sentimentos_normalizado = normalizar_sentimentos(sentimentos)    

    save_dictionary(valores_acao, 'valores_acao')
    save_dictionary(sentimentos_normalizado, 'sentimentos_normalizado')

    correlacao = get_correlacao(
        list(sentimentos.values()),
        list(valores_acao.values())
    )
    correlacao_normalizado = get_correlacao(
        list(sentimentos_normalizado.values()),
        list(valores_acao.values())
    )

    return correlacao, correlacao_normalizado
    
dataset = get_dataset('noticias_teste.csv')                
correlacao, correlacao_normalizado = gerar_correlacao(dataset)
print("teste manual ", correlacao)
print("teste manual normalizado ", correlacao_normalizado)

dataset = get_dataset('scikit_sentimentos.csv')
correlacao, correlacao_normalizado = gerar_correlacao(dataset)
print("teste previsão ", correlacao)
print("teste previsão normalizado ", correlacao_normalizado)