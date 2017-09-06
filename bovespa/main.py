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
    for registro in registros:
        registro.save()
    #Registro01.insert_many(registros).execute()

leitor = LeitorPeewee()
registros = leitor.ler("/home/eduardo/UEM/TCC/Git/TCC/bovespa/COTAHIST_M082017.TXT")
escrever(registros)

rows = Registro01.select().order_by(Registro01.preco_ultimo)
print(rows.count())