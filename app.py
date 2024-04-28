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
    #quero criar um arquivo txt para salvar as requisições processadas caso nao exista
    if not os.path.exists('requisicoes_processadas.txt'):
        with open('requisicoes_processadas.txt', 'w') as file:
            file.write("")
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
            
# Função para pega o usuario em outra tabela passando o id
def pegar_usuario_id(conn, id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM r910usu WHERE codent = {id}")
    usuario = cursor.fetchall()
    cursor.close()
    return usuario[0][2]

# Função para verificar novas requisições na tabela específica
def verificar_novas_requisicoes(conn, requisicoes_processadas):
    findListReq = []
    lastReq = requisicoes_processadas[0]
    cursor = conn.cursor()
    cursor.execute(f"SELECT usuario_id,requisicao_id,sequencia,um,quantidade,produto_id,descricao_produto,Observacao,deposito FROM {tabela} WHERE requisicao_id > {lastReq}")
    ultima_requisicao_bd = cursor.fetchall()
    cursor.close()
    
    if ultima_requisicao_bd:
        size_ultima_requisicao_bd = len(ultima_requisicao_bd)
        getRequisitante = ultima_requisicao_bd[0][0]
        fistReq = ultima_requisicao_bd[0][1]
        nomeRequisitante = pegar_usuario_id(conn, getRequisitante)
        
        for i in range(size_ultima_requisicao_bd):
            numeme = ultima_requisicao_bd[i][1]
            if numeme == fistReq:
                findListReq.append(ultima_requisicao_bd[i])            
   
    if findListReq:
        linhas_html = ""
        for linha in findListReq:
            detalhes_requisicao = "<tr>"
            for coluna in linha[1:]:
                detalhes_requisicao += f"<td>{coluna}</td>"
            detalhes_requisicao += "</tr>"
            linhas_html += detalhes_requisicao
        return linhas_html, fistReq, nomeRequisitante        
    return None


# Função para enviar e-mail
def enviar_email(assunto, tabela, nomeRequisitante):
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
        <p>Requisitante: 463</p>
        <p>Detalhes da Requisição:</p>
        <table>
            <thead>
                <tr>
                    <th>Requisição</th>
                    <th>Sequência</th>
                    <th>UM</th>
                    <th>Quantidade</th>
                    <th>ID Produto</th>
                    <th>Descrição</th>
                    <th>Observação</th>
                    <th>Depósito</th>
                </tr>
            </thead>
            <tbody>
                {tabela}
            </tbody>
        </table>
        <p>Att,<br>{nomeRequisitante}</p>
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
        print("Lista das requi salvar em arquivo: ", requisicoes_processadas)
        while True:
            nova_requisicao = verificar_novas_requisicoes(conn, requisicoes_processadas)
            # print(f"Requisições encontradas: {len(novas_requisicoes)}")
            if nova_requisicao:
                tabela, requisicao, nomeRequisitante = nova_requisicao
                # print("Tabela com os dados da requisição: ", tabela)
                assunto = f"Nova requisição gerada: {requisicao}"
                enviar_email(assunto, tabela, nomeRequisitante)
                # requisicoes_processadas.append(str(numeme))
                # salvar_requisicoes_processadas(requisicoes_processadas)
            else:
                print("Nenhuma nova requisição encontrada.")
            # Coloque um tempo de espera entre as verificações para não sobrecarregar o servidor
            time.sleep(60)  # Aguarda 60 segundos antes da próxima verificação
    else:
        print("Não foi possível conectar ao banco de dados. Verifique as configurações de conexão.")
