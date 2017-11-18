from registro01 import Registro01
import peewee

import os
import pandas as pd
import numpy as np


from sklearn import preprocessing


from scipy.stats.stats import pearsonr

import re
from datetime import datetime, timedelta

def save_dictionary(dictionary, name):
    np.save(
        os.path.join(os.path.dirname(__file__), '..//data//dics', name), 
        dictionary
    ) 

def get_dataset(filename):
    try:
        return pd.read_csv(
            os.path.join(os.path.dirname(__file__), '..//data//input', filename),
            usecols=['data', 'sentimento']
        )             
    except:
        dataset =  pd.read_csv(
            os.path.join(os.path.dirname(__file__), '..//data//input', filename),
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

def normalizar(dic, range):    
    df = pd.DataFrame(list(dic.items()), columns=['data', 'valor'])
    y = df['valor'].values.astype(float)
    y = y.reshape(-1,1)
    # Create a minimum and maximum processor object
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=range)

    # Create an object to transform the data to fit minmax processor
    y_scaled = min_max_scaler.fit_transform(y)

    # Run the normalizer on the dataframe            
    df['valor'] = y_scaled    
    return {row['data']: row['valor'] for _,row in df.iterrows()}

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

    valores_acao = {}
    sentimentos = {} 

    for index, row in dataset.iterrows():                
        data = re.sub(regex, subst, row['data'], 0)            
        data = data.strip()        
        data = datetime.strptime(data, "%Y%m%d").date()            
        if data not in sentimentos:
            sentimentos[data] = row['sentimento']        
        else:
            sentimentos[data] += row['sentimento']        
                    

    dates = list(sentimentos.keys())        
    dates.reverse()    
    for i, data_sentimento in enumerate(dates):                
        if i in [0,1]:
            data_acao = data_sentimento + timedelta(days=i+1)
        else:
            data_acao = dates[i]
                    
        acao = get_acao_petrobras(data_acao.strftime('%Y%m%d'))                
        while not acao:            
            data_acao = data_acao + timedelta(days=1)                        
            acao = get_acao_petrobras(data_acao.strftime('%Y%m%d'))                
            
        if (acao and data_sentimento not in valores_acao):       
            valores_acao[data_sentimento] = float(acao.preco_ultimo)
                                                            
    return valores_acao, sentimentos



def gerar_correlacao(dataset, arquivo_salvar):
    valores_acao, sentimentos = gerar_valores_e_sentimentos(dataset)
        
    import operator
        
#    max_range = max(valores_acao.items(), key=operator.itemgetter(1))[1]
#    min_range = min(valores_acao.items(), key=operator.itemgetter(1))[1]        

    max_range = 1
    min_range = -1

    sentimentos_normalizado = normalizar(sentimentos, (min_range, max_range))    
    #sentimentos_normalizado = normalizar_sentimentos(sentimentos)    
    acoes_normalizado = normalizar(valores_acao, (min_range, max_range))                
            
    save_dictionary(valores_acao, 'valores_acao_{}'.format(arquivo_salvar))    
    save_dictionary(sentimentos_normalizado, 'sentimentos_normalizado_{}'.format(arquivo_salvar))
    save_dictionary(acoes_normalizado, 'acoes_normalizado_{}'.format(arquivo_salvar))
    
    x = []
    y = []
    x_normalizado = []
    y_normalizada = []

    for data in sorted(sentimentos.keys()):                
        x.append(sentimentos[data])
        x_normalizado.append(sentimentos_normalizado[data])
        y.append(valores_acao[data])
        y_normalizada.append(acoes_normalizado[data])

    correlacao = get_correlacao(
        x,
        y
    )
    correlacao_normalizado = get_correlacao(
        x_normalizado,
        y_normalizada
    )

    return correlacao, correlacao_normalizado

def print_correlacao(campo,normal,pcorrelacao, text_file):
    if normal:
        print("{} & Sim & {:.2f}\\% & {:.2f}\\% \\\\".format(
            campo,
            pcorrelacao[0] * 100,
            pcorrelacao[1] * 100
        ), file=text_file)
    else:
        print("{} & Não & {:.2f}\\% & {:.2f}\\% \\\\".format(
            campo,
            pcorrelacao[0] * 100,
            pcorrelacao[1] * 100
        ), file=text_file)

    
    print("{} Correlação: {:.2f}, p-Value: {:.2f}".format(
            campo,
            pcorrelacao[0] * 100,
            pcorrelacao[1] * 100
    ))
    
with open("..//data//auxiliar//latex_correlação.txt", "w") as text_file:
    arquivos = [        
        'noticias_maio.csv',
        'noticias_junho.csv',
        'noticias_julho.csv',
        'noticias_agosto.csv',
        'noticias_setembro.csv',
        'noticias_outubro.csv'
    ]    
    for arquivo in arquivos:
        correlacao, correlacao_normalizado = gerar_correlacao(get_dataset(arquivo), arquivo)        
        campo = "Dados de " + arquivo[9:arquivo.find('.csv') ]                        
        print_correlacao(campo, True, correlacao_normalizado, text_file)        

    dataset = pd.concat([        
            get_dataset('noticias_maio.csv'),
            get_dataset('noticias_junho.csv'),
            get_dataset('noticias_julho.csv'),
            get_dataset('noticias_agosto.csv'),                
            get_dataset('noticias_setembro.csv'),
            get_dataset('noticias_outubro.csv'), 
        ], ignore_index=True 
    )

    correlacao, correlacao_normalizado = gerar_correlacao(dataset, 'geral')        
    print_correlacao("Dados geral", True, correlacao_normalizado, text_file)        