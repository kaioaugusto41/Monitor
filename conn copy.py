import sqlite3
from datetime import datetime
import time
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

data_atual = datetime.now()

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()


# COMANDO QUE PEGA O ÚLTIMO ID DA TABELA DE PRODUÇÃO
cursor.execute('SELECT id FROM dash_paradas ORDER BY id DESC LIMIT 1')
ultimo_id = int(cursor.fetchall()[0][0])
_id = ultimo_id+1

# COMANDO QUE ADICIONA A PRODUÇÃO NA TABELA DE PRODUÇÃO DA MÁQUINA 1
cursor.execute("INSERT INTO dash_paradas VALUES({}, '{}', {}, {})".format(_id, data_atual, 7, 1))
connection.commit()
time.sleep(2)
