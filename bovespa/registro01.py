import peewee

data_base = peewee.SqliteDatabase('bovespa.db')

class Registro01(peewee.Model):        
    data_pregao = peewee.DateField()
    codigo_bdi = peewee.CharField(max_length=2) 
    codigo_negociacao = peewee.CharField(max_length=12)
    tipo_mercado = peewee.IntegerField()
    nome_resumido = peewee.CharField(max_length=12)
    especificaco = peewee.CharField(max_length=10)
    prazo_termo = peewee.CharField(max_length=3)    
    moeda = peewee.CharField(max_length=4)
    preco_abertura = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_maximo = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_minimo = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_medio = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_ultimo = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_ofc = peewee.DecimalField(max_digits=11, decimal_places=2)
    preco_ofv = peewee.DecimalField(max_digits=11, decimal_places=2)
    total_negocios = peewee.IntegerField()
    quantidade_titulos = peewee.IntegerField()
    volume_titulos = peewee.DecimalField(max_digits=16, decimal_places=2)
    preexe = peewee.DecimalField(max_digits=11, decimal_places=2)
    indicador_cp = peewee.IntegerField()
    data_vencimento =  peewee.DateField()
    fator_cotacao = peewee.IntegerField()
    ptoexe  = peewee.DecimalField(max_digits=11, decimal_places=2)
    codigo_isin = peewee.CharField(max_length=12)
    dismes = peewee.IntegerField()
            
    class Meta:        
        database = data_base