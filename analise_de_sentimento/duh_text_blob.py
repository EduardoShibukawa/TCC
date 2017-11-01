import os
import pandas as pd
from textblob import TextBlob


def get_dataset(filename):
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), 'data', filename)        
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


dataset = get_dataset('noticias_teste.csv')
sentimento_titulo, sentimento_conteudo = sentiment(dataset)
output = pd.DataFrame(data={
    "data":dataset["data_atualizacao"],    
    "titulo":dataset["titulo"],    
    "sentimento_titulo":sentimento_titulo, 
})
output.to_csv(
    os.path.join(os.path.dirname(__file__), 'data', 'text_blob_sentimentos_titulo.csv')    
)    


output = pd.DataFrame(data={
    "data":dataset["data_atualizacao"],    
    "dtitulo":dataset["titulo"],    
    "sentimento_conteudo": sentimento_conteudo,
})
output.to_csv(
    os.path.join(os.path.dirname(__file__), 'data', 'text_blob_sentimentos_conteudo.csv')    
)    
