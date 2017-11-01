import numpy as np 

import plotly as ply
import plotly.graph_objs as go


def load_dictionary(name):
    return np.load(name).item(0)

valores_acao = load_dictionary('valores_acao.npy')
sentimentos_normalizado = load_dictionary('sentimentos_normalizado.npy')
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
ply.offline.plot({
    "data": [trace0, trace1], 
    "layout": go.Layout(
        title="Line Chart",        
        font=dict(family='Courier New, monospace', size=18, color='rgb(0,0,0)')
    )}, filename='teste_duh.html',image='jpeg'
)