import subprocess
import smtplib
from email.mime.text import MIMEText
threshold = 20
partition = '/'
def report_via_email():
    msg = MIMEText("Space has been increade")
    msg["Subject"] = "Low disk space warnning"
    msg["From"] = "example@gmail.com"
    msg["To"] = "example@gmail.com"
    with smtplib.SMTP("smtp.gmail.com",587) as server:
         server.ehlo()
         server.starttls()
         server.login("example@gmail.com","")
         server.sendmail("example@gmail.com","example@gmail.com",msg.as_string())
def check_once():
    df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)
    for line in df.stdout:
       spiltline = line.decode().split()
       if spiltline[5] == partition:
         if int(spiltline[4][:-1]) > threshold:
             report_via_email()
check_once()
