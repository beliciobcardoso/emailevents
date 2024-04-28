import time

def data_hora():
    return f"{time.localtime().tm_mday}/{time.localtime().tm_mon}/{time.localtime().tm_year} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"