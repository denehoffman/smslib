import smtplib
from smslib.receiver import Receiver
import re

class Sender:
    def __init__(self, email, password, smtp_server, port=587):
        self._email = None
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.port = port

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = self.validate_email(value)

    def validate_email(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if email_regex.match(email):
            return email
        else:
            print(f"Invalid email address: {email}")
            return None

    def check_credentials(self):
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP authentication error: {e}")
            print("This error often arises from password problems.")
            print("If you are using GMail with 2FA, you need to make")
            print("an App Password to use this package!")

    def send_message(self, message, receiver):
        to_email = receiver.email
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, to_email, message)
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP authentication error: {e}")
            print("This error often arises from password problems.")
            print("If you are using GMail with 2FA, you need to make")
            print("an App Password to use this package!")
        except smtplib.SMTPConnectError as e:
            print(f"SMTP connection error: {e}")
        except smtplib.SMTPHeloError as e:
            print(f"SMTP helo error: {e}")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"SMTP recipient refused error: {e}")
        except smtplib.SMTPSenderRefused as e:
            print(f"SMTP sender refused error: {e}")
        except smtplib.SMTPDataError as e:
            print(f"SMTP data error: {e}")
        except smtplib.SMTPException as e:
            print(f"SMTP error: {e}")
