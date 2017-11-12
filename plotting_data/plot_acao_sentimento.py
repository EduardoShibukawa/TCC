import numpy as np 

import plotly as ply
import plotly.graph_objs as go


def load_dictionary(name):
    return np.load('..//data//dics//' + name).item(0)

arquivos = [        
        'noticias_maio.csv',
        'noticias_junho.csv',
        'noticias_julho.csv',
        'noticias_agosto.csv',
        'noticias_setembro.csv',
        'noticias_outubro.csv'
]    

for arquivo in arquivos:
    campo = "Dados de " + arquivo[9:arquivo.find('.csv') ]        
    valores_acao = load_dictionary('acoes_normalizado_{}.npy'.format(arquivo))
    sentimentos_normalizado = load_dictionary('sentimentos_normalizado_{}.npy'.format(arquivo))
    # Create traces
    trace0 = go.Scatter(
        x = list(valores_acao.keys()),
        y = list(valores_acao.values()),
        mode = 'lines+markers',
        name = 'Valor Ação'
    )
    trace1 = go.Scatter(
        x = list(sentimentos_normalizado.keys()),    
        y = list(sentimentos_normalizado.values()),
        mode = 'lines+markers',
        name = 'Sentimento'
    )
    # Create chart 
    # Output will be stored as a html file. 
    # Whenever we will open output html file, one popup option will ask us about if want to save it in jpeg format.
    # Font family can be used in a layout to define font type, font size and font color for title           
    p = ply.offline.plot({
        "data": [trace0, trace1], 
        "layout": go.Layout(
            title="Ação X Sentimento - {}".format(campo),        
            font=dict(family='Courier New, monospace', size=18, color='rgb(0,0,0)')
        )}, filename='..//data//plot//{}.html'.format(campo.lower().replace("dados", "grafico").replace(" ", "_"))
    )
    
    