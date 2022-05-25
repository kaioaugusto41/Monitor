
def converteData(data):
    data_convertida =  '{}/{}/{} às {}:{}'.format(data[8:10], data[5:7], data[:4], data[11:13], data[14:])
    return data_convertida