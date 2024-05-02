import pyodbc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import dotenv
import os
import date_time
import logging

# Configuração do logger com info e error
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

dotenv.load_dotenv(dotenv.find_dotenv())



# Variáveis para as propriedades da conexão com o banco de dados
driver = '{SQL Server}'
server = os.getenv('server')
database = os.getenv('database')
username = os.getenv('user')
password = os.getenv('password')

# Função para conectar ao banco de dados SQL Server
def conectar_banco():
    while True:
        try:
            conn = pyodbc.connect(
                f'DRIVER={driver};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password};'
            )
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conn
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e} - {date_time.data_hora()}")
            logging.error(f"Erro ao conectar ao banco de dados: {e} - Verifique as configurações de conexão ou o banco de dados pode esta offline. {date_time.data_hora()}")
            time.sleep(sleep_DB)

# Função para exibir mensagem de bom dia, boa tarde ou boa noite
def saudacao():
    hora = time.localtime().tm_hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

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
        for requisicao_processada in requisicoes_processadas:
         file.write(f"{requisicao_processada}\n")
                
# Função para pega o usuario em outra tabela passando o id
def pegar_usuario_id(conn, id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT nomcom FROM r910usu WHERE codent = {id}")
    usuario = cursor.fetchall()
    cursor.close()
    return usuario[0][0]

def get_requisitante_id(conn, id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT nomusu FROM r999usu WHERE codusu = {id}")
    usuario = cursor.fetchall()
    cursor.close()
    return usuario[0][0]

# Função para verificar novas requisições na tabela específica
def verificar_novas_requisicoes(conn, requisicoes_processadas):
    findListReq = []
    lastReq = requisicoes_processadas[0]
    # print("Ultima requisição processada: ", lastReq)
    cursor = conn.cursor()
    cursor.execute(f"SELECT usueme,numeme,seqeme,unimed,qtdeme,codpro,cplpro,obseme,coddep FROM e207eme WHERE numeme > {lastReq}")
    ultima_requisicao_bd = cursor.fetchall()
    cursor.close()
    
    if ultima_requisicao_bd:
        size_ultima_requisicao_bd = len(ultima_requisicao_bd)
        getRequisitante = ultima_requisicao_bd[0][0]
        fistReq = ultima_requisicao_bd[0][1]
        nomeRequisitante = pegar_usuario_id(conn, getRequisitante)
        idRequisitante = get_requisitante_id(conn, getRequisitante)
        login = f"{getRequisitante} - {idRequisitante}"
        
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
        return linhas_html, fistReq, nomeRequisitante, login      
    return None


# Função para enviar e-mail
def enviar_email(assunto, tabela, nomeRequisitante, login):
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
        <p>Prezado(a), {saudacao()}!</p>
        <p>Uma nova requisição foi gerada!</p>
        <p>Requisitante: {login}</p>
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
        # print("Lista das requi salvar em arquivo: ", requisicoes_processadas)
        while True:
            nova_requisicao = verificar_novas_requisicoes(conn, requisicoes_processadas)
            # print(f"Requisições encontradas: {len(novas_requisicoes)}")
            if nova_requisicao:
                tabela, requisicao, nomeRequisitante, login = nova_requisicao
                # print("Tabela com os dados da requisição: ", tabela)
                assunto = f"Nova requisição gerada: {requisicao}"
                enviar_email(assunto, tabela, nomeRequisitante, login)
                requisicoes_processadas.insert(0, str(requisicao))
                # print("Requisições processadas: ", requisicoes_processadas)
                salvar_requisicoes_processadas(requisicoes_processadas)
                print(f"Nova requisição encontrada: {requisicao}. E-mail enviado com sucesso!", date_time.data_hora())
                time.sleep(10)  # Aguarda 10 segundos antes de verificar a próxima requisição
            else:
                print("Nenhuma nova requisição encontrada.", date_time.data_hora())
                # Coloque um tempo de espera entre as verificações para não sobrecarregar o servidor
                time.sleep(60)  # Aguarda 60 segundos antes da próxima verificação
    else:
        print("Não foi possível conectar ao banco de dados. Verifique as configurações de conexão.", date_time.data_hora())
