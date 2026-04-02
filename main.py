import pandas as pd
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
# configurações de email
load_dotenv()
MEU_EMAIL = os.getenv("MEU_EMAIL")
SENHA_APP = os.getenv("SENHA_APP")


def enviar_emails_b2b():
    try:
        LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBIJi6cimqdAGvngf4T4wXVmFybqme2ZFDkwdKIMThx_TOu0uLm19BYRdH2VKipSAa_u4FXjIR_t0S/pub?output=csv"
        tabela = pd.read_csv(LINK_GOOGLE_SHEETS)
        print("COLUNAS QUE O PYTHON ACHOU:", tabela.columns)
    except FileNotFoundError:
        print(
            'Arquivo clientes.xlsx não encontrado. Verifique o caminho e tente novamente.')
        return
    # carregar o template html
    try:
        with open("template.html", "r", encoding="utf-8") as arquivo:
            template_html = arquivo.read()
    except FileNotFoundError:
        print(
            'Arquivo template.html não encontrado. Verifique o caminho e tente novamente.')
        return
    # conectar servidor ao gmail
    print("conectando ao servidor de email... ")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MEU_EMAIL, SENHA_APP)
    except Exception as e:
        print(f"Erro ao conectar ao servidor de email: {e}")
        return
    # processar cada cliente da planilha
    print("iniciando envio de emails... ")
    for index, linha in tabela.iterrows():
        nome = str(linha['Nome'])
        email_destinado = str(linha['Email'])
        empresa = str(linha['Empresa'])
        tema_livros = str(linha['Tema_Livros'])
        desconto = str(linha['Desconto'])

        
    # personalizar o template
        corpo_email = template_html.replace("{nome}", nome)
        corpo_email = corpo_email.replace("{email}", email_destinado)
        corpo_email = corpo_email.replace("{empresa}", empresa)
        corpo_email = corpo_email.replace("{tema_livros}", tema_livros)
        corpo_email = corpo_email.replace("{desconto}", desconto)
        # criar email
        msg = EmailMessage()
        msg['Subject'] = f"Parceria literária: Uma oportunidade para a {empresa}"
        msg['From'] = MEU_EMAIL
        msg['To'] = email_destinado
        msg.set_content("Abra este email em um cliente que suporte HTML.") 
        msg.add_alternative(corpo_email, subtype='html')
        # enviar email
        try: 
            server.send_message(msg)
            print(f"Email enviado para {email_destinado}")
        except Exception as e:
            print(f"Erro ao enviar email para {email_destinado}: {e}")
    # fechar conexão
    server.quit()
    print("Envio de emails concluído.")

# Executar a função
if __name__ == "__main__":
    enviar_emails_b2b()