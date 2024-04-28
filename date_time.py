import time

ano = time.localtime().tm_year
mes = time.localtime().tm_mon
dia = time.localtime().tm_mday
hora = time.localtime().tm_hour
min = time.localtime().tm_min
seg = time.localtime().tm_sec

def data_hora():
    return f"{dia}/{mes}/{ano} {hora}:{min}:{seg}"