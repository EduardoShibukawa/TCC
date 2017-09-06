import peewee
from registro01 import Registro01

rows = Registro01.select().order_by(Registro01.preco_ultimo)
print(rows.count())
for row in rows:
    print(row.__dict__)