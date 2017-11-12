import os
import pandas as pd
from textblob import TextBlob

def to_latex(dataset):
    with open("latex_text_blob.txt", "w") as text_file:
        for index, row in dataset.iterrows():                
            print("{} & {} & {:4f} & {:4f} \\\\".format(
                row['data'],
                row['dtitulo'][:80].replace('$', '\\$').replace('%', '\\%') + ' ...',
                row['sentimento'][0],
                row['sentimento'][1]
            ), file=text_file)            

def get_dataset(filename):
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..//data//input', filename)        
    )    

def get_translated_blob(text):
    blob = TextBlob(text)
    return blob.translate(from_lang='pt-br', to="en")

def sentiment(dataset):
    sentimento_titulo = []
    sentimento_conteudo = []
    for index, row in dataset.iterrows():    
        blob_titulo = get_translated_blob(row['titulo'])
        blob_conteudo = get_translated_blob(row['conteudo'])
                
        sentimento_titulo.append(blob_titulo.sentiment)
        sentimento_conteudo.append(blob_conteudo.sentiment)
    
    return sentimento_titulo, sentimento_conteudo


dataset = pd.concat([        
#        get_dataset('noticias_maio.csv'),
#        get_dataset('noticias_junho.csv'),
#        get_dataset('noticias_julho.csv'),
#        get_dataset('noticias_agosto.csv'),                
#        get_dataset('noticias_setembro.csv'),
        get_dataset('noticias_outubro.csv'),

    ], ignore_index=True 
)

sentimento_titulo, sentimento_conteudo = sentiment(dataset)

output = pd.DataFrame(data={
    "data":dataset["data_atualizacao"],    
    "dtitulo":dataset["titulo"],    
    "sentimento": sentimento_conteudo    
})

output.to_csv(
    os.path.join(os.path.dirname(__file__), '..//data//output', 'sentimentos_text_blob.csv')    
)    

to_latex(output)