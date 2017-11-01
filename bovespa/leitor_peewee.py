from registro01 import Registro01

def to_float(value):
    return float(value) / 100

def new_registro01(linha):
    reg01 = Registro01()    
    reg01.data_pregao = int(linha[2:10])
    reg01.codigo_bdi = linha[10:12].strip()
    reg01.codigo_negociacao = linha[12:24].strip()
    reg01.tipo_mercado = int(linha[24:27])
    reg01.nome_resumido = linha[27:39].strip()
    reg01.especificaco = linha[39:49].strip()
    reg01.prazo_termo = linha[49:52].strip()
    reg01.moeda = linha[52:56].strip()
    reg01.preco_abertura = to_float(linha[57:69])
    reg01.preco_maximo = to_float(linha[69:82])
    reg01.preco_minimo = to_float(linha[82:95])
    reg01.preco_medio = to_float(linha[95:108])
    reg01.preco_ultimo = to_float(linha[108:121])
    reg01.preco_ofc = to_float(linha[121:134])
    reg01.preco_ofv = to_float(linha[134:147])
    reg01.total_negocios = int(linha[147:152])
    reg01.quantidade_titulos = int(linha[152:170])
    reg01.volume_titulos = to_float(linha[170:188])
    reg01.preexe = to_float(linha[188:201])
    reg01.indicador_cp = int(linha[201:202])
    reg01.data_vencimento =  int(linha[202:210])
    reg01.fator_cotacao = int(linha[210:217])
    reg01.ptoexe  = to_float(linha[217:230])
    reg01.codigo_isin = linha[230:242].strip()
    reg01.dismes = int(linha[242:245])
    return reg01


class LeitorPeewee(object):    
    def ler(self, arquivo): 
        registros = []
        arquivo = open(arquivo, "r")    
        for linha in arquivo.readlines():
            tipo_registro = int(linha[:2])
            if tipo_registro == 1:
                 registros.append(new_registro01(linha))
        return registros