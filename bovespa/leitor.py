def to_float(value):
    return float(value) / 100
       
class Registro01(object):        
    def __init__(self, linha):        
        self.data_pregao = int(linha[2:10])
        self.codigo_bdi = linha[10:12]
        self.codigo_negociacao = linha[12:24]
        self.tipo_mercado = int(linha[24:27])
        self.nome_resumido = linha[27:39]
        self.especificaco = linha[39:49]
        self.prazo_termo = linha[49:52]
        self.moeda = linha[52:56]
        self.preco_abertura = to_float(linha[57:69])
        self.preco_maximo = to_float(linha[69:82])
        self.preco_minimo = to_float(linha[82:95])
        self.preco_medio = to_float(linha[95:108])
        self.preco_ultimo = to_float(linha[108:121])
        self.preco_ofc = to_float(linha[121:134])
        self.preco_ofv = to_float(linha[134:147])
        self.total_negocios = int(linha[147:152])
        self.quantidade_titulos = int(linha[152:170])
        self.volume_titulos = to_float(linha[170:188])
        self.preexe = to_float(linha[188:201])
        self.indicador_cp = int(linha[201:202])
        self.data_vencimento =  int(linha[202:210])
        self.fator_cotacao = int(linha[210:217])
        self.ptoexe  = to_float(linha[217:230])
        self.codigo_isin = linha[230:242]
        self.dismes = int(linha[242:245])
        
    def __str__(self):
        return str(self.__dict__)        

    def __repr__(self):
        return self.__str__()

class Leitor(object):    
    def ler(self, arquivo): 
        registros = []
        arquivo = open(arquivo, "r")    
        for linha in arquivo.readlines():
            tipo_registro = int(linha[:2])
            if tipo_registro == 1:
                 registros.append(Registro01(linha).__dict__)

        return registros