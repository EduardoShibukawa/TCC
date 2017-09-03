from pprint import pprint
from leitor import Leitor
from escritor import Escritor

leitor = Leitor()
escritor = Escritor("/home/eduardo/UEM/TCC/Git/TCC/bovespa/meu_arquivo")

registros = leitor.ler("/home/eduardo/UEM/TCC/Git/TCC/bovespa/COTAHIST_M082017.TXT")
for registro in registros:
    pprint(registro.__dict__)

escritor.escrever(registros)