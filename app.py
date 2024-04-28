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

tabela = 'requisicoes'
column_number_requisicao = 'requisicao_id'

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

# Função para carregar as requisições processadas a partir do arquivo
def carregar_requisicoes_processadas():
    try:
        with open('requisicoes_processadas.txt', 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []

# Função para salvar as requisições processadas no arquivo
def salvar_requisicoes_processadas(requisicoes_processadas):
    with open('requisicoes_processadas.txt', 'w') as file:
        for req in requisicoes_processadas:
            file.write(f"{req}\n")

# Função para verificar novas requisições na tabela específica
def verificar_novas_requisicoes(conn, requisicoes_processadas):
    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 * FROM {tabela}")
    ultima_requisicao_bd = cursor.fetchone()
    print(ultima_requisicao_bd)

    # if ultima_requisicao_bd:
    #     numeme = ultima_requisicao_bd[0]
    #     if str(numeme) not in requisicoes_processadas:
    #         requisitante = ultima_requisicao_bd[1]  # Exemplo: coluna do requisitante
    #         detalhes_requisicao = ""  # Aqui você precisa formatar os detalhes da requisição como uma tabela HTML
    #         # Exemplo: formatar os detalhes da requisição como uma tabela HTML
    #         for linha in ultima_requisicao_bd[2:]:
    #             detalhes_requisicao += "<tr>"
    #             for coluna in linha:
    #                 detalhes_requisicao += f"<td>{coluna}</td>"
    #             detalhes_requisicao += "</tr>"
    #         return numeme, requisitante, detalhes_requisicao
    return None


# Função para enviar e-mail
def enviar_email(assunto, corpo):
    # Configurar servidor SMTP
    servidor_smtp = os.getenv('smtp_server')
    porta_smtp = os.getenv('smtp_port')
    usuario = os.getenv('smtp_user')
    senha = os.getenv('smtp_password')

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['To'] = os.getenv('email_destinatario')
    msg['Subject'] = assunto
    
    # Corpo do e-mail em formato HTML
    corpo_email = f"""
    <html>
    <head>
        <style>
            table {{
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <p>Prezado(a), Bom dia!</p>
        <p>Uma nova requisição foi gerada!</p>
        <p>Requisitante: {corpo}</p>
        <p>Detalhes da Requisição:</p>
        <table>
            <thead>
                <tr>
                    <th>Sequência</th>
                    <th>ID Produto</th>
                    <th>Descrição</th>
                    <th>Quantidade</th>
                    <th>UM</th>
                    <th>Depósito</th>
                    <th>Observação</th>
                </tr>
            </thead>
            <tbody>
            <tr>
                <td>1</td>
                <td>123</td>
                <td>Produto A</td>
                <td>10</td>
                <td>UN</td>
                <td>Depósito 1</td>
                <td>Observação 1</td>
            </tr>
            <tr>
                <td>2</td>
                <td>123</td>
                <td>Produto B</td>
                <td>20</td>
                <td>UN</td>
                <td>Depósito 1</td>
                <td>Observação 2</td>
                </tr>
            </tbody>
        </table>
        <p>Att,<br>Nome do Requisitante</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(corpo_email, 'html'))
    
    # Conectar e enviar e-mail
    with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
        server.starttls()
        server.login(usuario, senha)
        server.send_message(msg)

# Main
if __name__ == "__main__":
    conn = conectar_banco()
    if conn:
        requisicoes_processadas = carregar_requisicoes_processadas()
        while True:
            nova_requisicao = verificar_novas_requisicoes(conn, requisicoes_processadas)
            # print(f"Requisições encontradas: {len(novas_requisicoes)}")
            print(nova_requisicao)
            if nova_requisicao:
                numeme, requisitante, detalhes = nova_requisicao
                assunto = f"Nova requisição gerada: {numeme}"
                corpo = (numeme, requisitante, detalhes)
                # enviar_email(assunto, corpo)
                requisicoes_processadas.append(str(numeme))
                salvar_requisicoes_processadas(requisicoes_processadas)
            else:
                print("Nenhuma nova requisição encontrada.")
            # Coloque um tempo de espera entre as verificações para não sobrecarregar o servidor
            time.sleep(10)  # Aguarda 60 segundos antes da próxima verificação
    else:
        print("Não foi possível conectar ao banco de dados. Verifique as configurações de conexão.")
