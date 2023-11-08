import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


load_dotenv()
email_remetente = os.getenv('EMAIL_REMETENTE')
senha_remetente = os.getenv('SENHA_REMETENTE')


def enviar_email(destinatario, assunto, conteudo):

    conexao_smtp = None

    msg = MIMEMultipart()
    msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))
    msg['Subject'] = assunto

    try:
        conexao_smtp = smtplib.SMTP('smtp.office365.com', 587)
        conexao_smtp.starttls()
        conexao_smtp.login(email_remetente, senha_remetente)
        conexao_smtp.sendmail(email_remetente, destinatario, msg.as_string())

    except smtplib.SMTPException as erro:
        raise erro

    finally:
        if conexao_smtp:
            conexao_smtp.quit()
