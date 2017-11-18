import os


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_dataset(filename):
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..//data//input', filename),
        header=None        
    )                 

def plot(data):    
    plt.clf()
    svm = sns.heatmap(data, annot=True, fmt='5.2f', cmap='coolwarm', linecolor='white', linewidths=0)        
    plt.yticks(rotation=0) 
    svm.figure.tight_layout()    
    return svm.get_figure()        

dataset = get_dataset('correlacao.csv')
dataset.rename(columns={0: 'fonte', 1: 'dias', 2: 'correlacao', 3: 'pvalue'}, inplace=True)    
for c in ['fonte', 'dias']:
    dataset[c] = dataset[c].astype('category')

pivot_correlacao = dataset.pivot_table(index='fonte', columns='dias', values='correlacao')
pivot_pvalue = dataset.pivot_table(index='fonte', columns='dias', values='pvalue')


plot(pivot_correlacao).savefig('..//data//plot//heatmap_correlacao.png', dpi=400)
plot(pivot_pvalue).savefig('..//data//plot//heatmap_pvalue.png', dpi=400)
