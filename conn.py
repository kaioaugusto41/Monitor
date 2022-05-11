import sqlite3
from datetime import datetime
import time

data_atual = datetime.now()

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

for i in range(0, 250):

    # COMANDO QUE PEGA O ÚLTIMO ID DA TABELA DE PRODUÇÃO
    cursor.execute('SELECT id FROM dash_producao ORDER BY id DESC LIMIT 1')
    ultimo_id = int(cursor.fetchall()[0][0])
    _id = ultimo_id+1

    # COMANDO QUE ADICIONA A PRODUÇÃO NA TABELA DE PRODUÇÃO DA MÁQUINA 1
    cursor.execute("INSERT INTO dash_producao VALUES({}, '{}', 1, '{}', 4)".format(_id, i, data_atual))
    connection.commit()
    time.sleep(5)
