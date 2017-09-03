class Escritor(object):
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def escrever(self, registros): 
        arquivo = open(self.arquivo, 'w')        
        for registro in registros:
            arquivo.write("{}\n".format(registro))                 
        arquivo.close()