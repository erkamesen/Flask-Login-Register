from smtplib import SMTP




class MailSender:
    
    def __init__(self, token, sender_mail, 
                 mail_server="smtp.gmail.com", port=587):
        
        self.token = token
        self.sender_mail = sender_mail
        self.mail_server = mail_server
        self.port = port
        
    def send_password_link(self, receiver, link):
            with SMTP(self.mail_server, self.port) as connection:  
                connection.starttls()  
                connection.login(self.sender_mail, password=self.token)  
                connection.sendmail(from_addr=self.sender_mail,
                                                to_addrs=receiver,
                                                msg=f"Subject:Reset Password!\n\nYou can reset your password by following the link below:\n\n{link}")
    
    def send_activation_code(self, receiver, code):
            with SMTP(self.mail_server, self.port) as connection:  
                connection.starttls()  
                connection.login(self.sender_mail, password=self.token)  
                connection.sendmail(from_addr=self.sender_mail,
                                                to_addrs=receiver,
                                                msg=f"Subject:Activation Code!\n\nYou can complete your registration with the 6 digit code below:\n\n{code}")
    


