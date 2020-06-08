import smtplib
import webbrowser as wb
def send_mail_with_a_twu():
    print("Who is the sender of this email?: ")
    sender=input()
    print("What is your 16 digit passcode?: ")
    passcode=input()
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender,passcode)
    print("What is the subject of your email?: ")
    subject=input()
    print("What is the body of your email?: ")
    body=input()
    msg=f"subject: {subject}\n\n{body}"
    print("Who is the reciever of this email?: ")
    rec=input()
    server.sendmail(
         sender,
         rec,
         msg)
    server.quit() 
    gmail="www.gmail.com"
    print("Do you want to open Gmail: ")
    x=input()
    if x=="yes":
        wb.open(gmail)
        print("This email has been sent: ")
    if x=="no":
        print('This email has been sent: ')
send_mail_with_a_twu()

#pass=hpgtndgwkpyfkcuw