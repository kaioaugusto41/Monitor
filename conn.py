
import pandas as pd
import sqlite3
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
import time
from datetime import datetime



connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

while True:
    c = ModbusClient()
    c.host("192.168.0.5")
    c.port(502)
    data_atual = datetime.now()

    if not c.open():
        print('Não foi possível obter o status da linhaaa')
    if c.is_open():
        status_linha = c.read_holding_registers(5409, 1)
        if status_linha:
            cursor.execute('SELECT id FROM dash_producao ORDER BY id DESC LIMIT 1')
            ultimo_id = int(cursor.fetchall()[0][0])
            _id = ultimo_id+1
            cursor.execute("INSERT INTO dash_producao VALUES({}, '{}', {}, '{}', {})".format(_id, _id, _id, data_atual, 7))
            connection.commit()
            print('foi')
        else:
            print('Não foi possível obter o status da linha')
    time.sleep(1)



    # COMANDO QUE PEGA O ÚLTIMO ID DA TABELA DE PRODUÇÃO
    

    # COMANDO QUE ADICIONA A PRODUÇÃO NA TABELA DE PRODUÇÃO DA MÁQUINA 1
    

    # simulando dados recebidos e criando um data frame

    

 
