import smtplib, ssl
import email.message
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart

from json import load


def send_email_verification (emailTo, link):
  with open ('smtpConfig.json') as file:
    data= load(file)
    
  email_content = f"""
    <html>
    <head></head>
    <body>
    <h1>Bienvenido a <img src="{{url_for('static', filename='img/Recibes-Logo150x42.jpg')}}" alt=""></h1>
    <br />
    <p>Favor hacer click en el siguiente enlace para verificar tu identidad</p>
    <a href="{link}">Enlace de Verificación</a>
    <p>Gracias</p>
    </body>
    </html>
    """


  msg = MIMEMultipart('alternative')  
  

  msg.attach(MIMEText(email_content,'html'))

  
  msg['Subject'] = 'Bienvenido a APHS. Corro de Verificación'
  msg['From'] = data['smtp'][0]['from']
  msg['To'] = emailTo
  password = data['smtp'][0]['pwd']
  msg.add_header('Content-Type', 'text/html')
  
  
  s = smtplib.SMTP(host=data['smtp'][0]['host'],port=data['smtp'][0]['port'])
  s.starttls()
  
  # Login Credentials for sending the mail
  s.login(msg['From'], password)
  
  s.sendmail(msg['From'], [msg['To']], msg.as_string())
  s.quit()
  return 