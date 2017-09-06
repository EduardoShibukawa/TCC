import sqlite3


class Connect(object):
    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            print("Banco:", db_name)
            # lendo a versão do SQLite
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            # imprimindo a versão do SQLite
            print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Erro ao abrir banco.")                        

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class EscritorSQLLite(object):
    def __init__(self):
        self.tb_name = 'Registro01'
        self.db = Connect('bovespa.db')        

    def close_connection(self):
        self.db.close_db()

    def criar_schema(self, schema_name='sql/registro01_schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False

        print("Tabela %s criada com sucesso." % self.tb_name)
        

if __name__ == '__main__':
    escritor = EscritorSQLLite()
    escritor.criar_schema()
    escritor.close_connection()        
