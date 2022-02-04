import smtplib, ssl


port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "lopezc.diego@gmail.com"
password = "522leteo"

def sendemail (message, receiver_email):

  context = ssl.create_default_context()
  with smtplib.SMTP(smtp_server, port) as server:  
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
  
  