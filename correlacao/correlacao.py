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

def gerar_valores_e_sentimentos(dataset, dias):
    regex = r"(\d{2})\/(\d{2})\/(\d{4})"
    subst = r"\3\2\1"

    sentimentos = {}
    valores_acao = {}
    for index, row in dataset.iterrows():        
        data = re.sub(regex, subst, row['data'], 0)            
        data = data.strip()        
        data = datetime.strptime(data, "%Y%m%d").date() 
        if data not in sentimentos:
            sentimentos[data] = row['sentimento']        
        else:
            sentimentos[data] += row['sentimento']
                
        data_acao = data + timedelta(days=dias)
        acao = get_acao_petrobras(data_acao.strftime('%Y%m%d'))                        
        while not acao:
            data_acao = data_acao + timedelta(days=1)
            acao = get_acao_petrobras(data_acao.strftime('%Y%m%d'))

        if (acao and data not in valores_acao):
            valores_acao[data] = float(acao.preco_ultimo)    

    return valores_acao, sentimentos


def gerar_correlacao(dataset, arquivo_salvar, dias):
    valores_acao, sentimentos = gerar_valores_e_sentimentos(dataset, dias)
        
    import operator
        
    max_range = 1 #max(valores_acao.items(), key=operator.itemgetter(1))[1]
    min_range = -1 #min(valores_acao.items(), key=operator.itemgetter(1))[1]        

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

def save_to_latex_format(campo,dias,pcorrelacao, text_file):    
    print("{:20s} & {:0} & {:5.2f}\\% & {:5.2f}\\% \\\\".format(
        campo,
        dias,
        pcorrelacao[0] * 100,
        pcorrelacao[1] * 100
    ), file=text_file)    

    print("{:20s} Dias {:0} Correlação: {:5.2f}, p-Value: {:5.2f}".format(
            campo,
            dias,
            pcorrelacao[0] * 100,
            pcorrelacao[1] * 100
    ))    


def save_to_csv(campo,dias,pcorrelacao, csv_file):    
    print("{:20s},{:0},{:5.2f},{:5.2f}".format(
        campo,
        dias,
        pcorrelacao[0] * 100,
        pcorrelacao[1] * 100
    ), file=csv_file)    



text_file = open("..//data//auxiliar//latex_correlacao.txt", "w")
csv_file = open("..//data//input//correlacao.csv", "w")

arquivos = [        
    'noticias_maio.csv',
    'noticias_junho.csv',
    'noticias_julho.csv',
    'noticias_agosto.csv',
    'noticias_setembro.csv',
    'noticias_outubro.csv',
    'sentimentos_scikit.csv'
]    

#for dias in range(0,6):    
for dias in range(5,-1,-1):
    i = 0
    for arquivo in arquivos:
        i = i + 1
        campo = "{} - Dados de {}".format(i, arquivo[9:arquivo.find('.csv')])        
        campo = campo.replace("de os_scikit", "da previsão")
        #campo = "Dados de {}".format(arquivo[9:arquivo.find('.csv')])
        correlacao, correlacao_normalizado = gerar_correlacao(get_dataset(arquivo), arquivo, dias)
        save_to_latex_format(campo, dias, correlacao_normalizado, text_file)        
        save_to_csv(campo, dias, correlacao_normalizado, csv_file)        
dataset = pd.concat([        
        get_dataset('noticias_maio.csv'),
        get_dataset('noticias_junho.csv'),
        get_dataset('noticias_julho.csv'),
        get_dataset('noticias_agosto.csv'),                
        get_dataset('noticias_setembro.csv'),
        get_dataset('noticias_outubro.csv'), 
    ], ignore_index=True 
)

campo = "8 - Dados geral"
for dias in range(5,-1,-1):
#campo = "Dados geral"
#for dias in range(0,8):
    correlacao, correlacao_normalizado = gerar_correlacao(dataset, 'geral', dias)
    save_to_latex_format(campo, dias, correlacao_normalizado, text_file)        
    save_to_csv(campo, dias, correlacao_normalizado, csv_file)            
text_file.close()
csv_file.close()
