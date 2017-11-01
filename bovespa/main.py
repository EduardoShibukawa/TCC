import peewee
from leitor import Leitor
from leitor_peewee import LeitorPeewee
from registro01 import Registro01


def criar_tabela():
    try:
        Registro01.create_table()
    except peewee.OperationalError:
        print('Tabela Registro01 já existe!')

def escrever(registros):
    criar_tabela()    
    atual = 0
    for registro in registros:
        atual += 1
        print("Salvando {}".format(atual))
        #print("Salvando {} de {}".format(atual, count_registros))
        registro.save()
    #Registro01.insert_many(registros).execute()

leitor = LeitorPeewee()
registros = leitor.ler("/home/eduardo/UEM/GIT/TCC/data/COTAHIST_A2017.TXT")
registros = filter(lambda r: r.codigo_negociacao.startswith('PETR4'), registros)

escrever(registros)

rows = Registro01.select().order_by(Registro01.preco_ultimo)
print(rows.count())