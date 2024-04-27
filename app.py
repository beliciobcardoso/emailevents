import pyodbc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

# Variáveis para as propriedades da conexão com o banco de dados
driver = '{SQL Server}'
server = os.getenv('server')
database = os.getenv('database')
username = os.getenv('user')
password = os.getenv('password')

# Função para conectar ao banco de dados SQL Server
def conectar_banco():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para verificar novas requisições na tabela específica
def verificar_requisicoes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM e207eme WHERE numeme IS NOT NULL")
    rows = cursor.fetchall()
    return rows

# Função para enviar e-mail
def enviar_email(assunto, corpo):
    # Configurar servidor SMTP
    servidor_smtp = 'smtp.example.com'
    porta_smtp = 587
    usuario = 'seu_email@example.com'
    senha = 'sua_senha'

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['To'] = 'destinatario@example.com'
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    # Conectar e enviar e-mail
    with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
        server.starttls()
        server.login(usuario, senha)
        server.send_message(msg)

# Main
# if __name__ == "__main__":
#     conn = conectar_banco()
#     if conn:
#         while True:
#             novas_requisicoes = verificar_requisicoes(conn)
#             if novas_requisicoes:
#                 for requisicao in novas_requisicoes:
#                     assunto = "Nova requisição detectada"
#                     corpo = f"Detalhes da requisição: {requisicao}"
#                     enviar_email(assunto, corpo)
#             else:
#                 print("Nenhuma nova requisição encontrada.")
#             # Coloque um tempo de espera entre as verificações para não sobrecarregar o servidor
#             time.sleep(60)  # Aguarda 60 segundos antes da próxima verificação
#     else:
#         print("Não foi possível conectar ao banco de dados. Verifique as configurações de conexão.")
