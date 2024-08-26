import time

# Função para exibir mensagem de bom dia, boa tarde ou boa noite
def saudacao():
    hora = time.localtime().tm_hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"