from smslib import Sender as _Sender
from smslib import Receiver as _Receiver
import argparse as _argparse
import getpass as _getpass
from pathlib import Path as _Path
try:
    import tomllib as _tomllib
except ModuleNotFoundError:
    import tomli as _tomllib
import os as _os

class Notifier:
    def __init__(self):
        self.rcpath = _Path.home() / _Path(".smslibrc.toml")
        optpath = _os.getenv("SMSLIBRC")
        if optpath:
            self.rcpath = _Path(optpath)
        if self.rcpath.exists():
            self.rcconfig = _tomllib.loads(self.rcpath.read_text(encoding="utf-8"))
        else:
            self.rcconfig = {"senders": dict(), "receivers": dict()}

    def cli(self):
        desc_string = f"""Send an SMS via email

Available SMS providers: {', '.join(_Receiver.GATEWAYS.keys())}
        """
        parser = _argparse.ArgumentParser(description=desc_string)
        parser.add_argument("message", help="Message string to send")
        parser.add_argument("--sender", help=f"Sender name from {self.rcpath}")
        parser.add_argument("--receiver", help=f"Receiver name from {self.rcpath}")
        parser.add_argument("--email", help="Sender's email address")
        parser.add_argument("--password", help="Sender's password")
        parser.add_argument("--smtp-server", help="Sender's SMTP server")
        parser.add_argument("--port", default=587, help="Sender's SMTP server port")
        parser.add_argument("--phone-number", help="Receiver's phone number")
        parser.add_argument("--provider", help="Receiver's phone provider")
        parser.add_argument("--confirm", action="store_true", help="Print confirmation after sending message")
        args = parser.parse_args()
        rcsenders = self.rcconfig.get("senders", dict())
        rcreceivers = self.rcconfig.get("receivers", dict())
        sender_email = None
        sender_password = None
        sender_smtp_server = None
        sender_port = None
        receiver_phone_number = None
        receiver_provider = None
        receiver_email = None
        if args.sender:
            if args.sender in rcsenders:
                sender_email = rcsenders[args.sender].get("email")
                sender_password = rcsenders[args.sender].get("password")
                sender_smtp_server = rcsenders[args.sender].get("smtp_server")
                sender_port = rcsenders[args.sender].get("port")
            else:
                print(f"{args.sender} was not found in {self.rcpath}")
                return
        if args.receiver:
            if args.receiver in rcreceivers:
                receiver_phone_number = rcreceivers[args.receiver].get("phone_number")
                receiver_provider = rcreceivers[args.receiver].get("provider")
                receiver_email = rcreceivers[args.receiver].get("email") # optional, but use if provided
        if args.email:
            sender_email = args.email
        if args.password:
            sender_password = args.password
        if args.smtp_server:
            sender_smtp_server = args.smtp_server
        if args.port:
            sender_port = args.port
        if args.phone_number:
            receiver_phone_number = args.phone_number
        if args.provider:
            receiver_provider = args.provider
        while not sender_email:
            sender_email = input("Enter the sender's email address: ")
        while not sender_password:
            sender_password = _getpass.getpass(prompt="Enter the sender's email password: ")
        while not sender_smtp_server:
            sender_smtp_server = input("Enter the sender's SMTP server: ")
        sender = _Sender(sender_email, sender_password, sender_smtp_server, sender_port)
        sender.check_credentials()
        receiver = None
        if not receiver_email:
            while not receiver_phone_number:
                receiver_phone_number = input("Enter the receiver's phone number: ")
            if not receiver_provider:
                print(f"Available providers: {', '.join(_Receiver.GATEWAYS.keys())}")
            while not receiver_provider:
                receiver_provider = input("Enter the receiver's phone service provider: ")
            receiver = _Receiver(receiver_phone_number, receiver_provider)
        else:
            receiver = _Receiver(None, None, email=receiver_email)
        sender.send_message(args.message, receiver)
        if args.confirm:
            print("Message sent!")

def main():
    Notifier().cli()
