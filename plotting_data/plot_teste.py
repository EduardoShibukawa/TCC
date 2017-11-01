import numpy as np 

import plotly as ply
from plotly.graph_objs import *

def load_dictionary(name):
    return np.load(name).item(0)

valores_acao = load_dictionary('valores_acao.npy')
sentimentos_normalizado = load_dictionary('sentimentos_normalizado.npy')

trace = Heatmap(
        z=[
            list(valores_acao.values()),
            list(sentimentos_normalizado.values())
        ],
        x=list(valores_acao.keys()),
        y=['Valores Acao', 'Sentimentos']
)

data=[trace]
fig = Figure(data=data)
ply.offline.plot(fig, filename='teste_duh.html',image='jpeg')