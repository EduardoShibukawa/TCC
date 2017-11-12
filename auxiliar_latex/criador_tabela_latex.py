import os
import pandas as pd
from textblob import TextBlob

def to_latex(dataset, arquivo):
    with open("..//data//auxiliar//{}.txt".format(arquivo), "w") as text_file:
        for index, row in dataset.iterrows():                
            print("{} & {} & {} \\\\".format(
                row['data'],
                row['titulo'][:90].replace('$', '\\$').replace('%', '\\%') + ' ...',
                row['sentimento'],                
            ), file=text_file)            


def get_dataset(filename):    
    dataset = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..//data', filename)
    )    
    dataset.rename(columns={'data_atualizacao': 'data'}, inplace=True)

    return dataset

nome_arquivo = 'sentimentos_scikit'
dataset = get_dataset('output//{}.csv'.format(nome_arquivo))
to_latex(dataset, nome_arquivo)