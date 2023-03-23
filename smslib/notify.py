from smslib import Sender, Receiver
import argparse
import getpass
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import os

class Notifier:
    def __init__(self):
        self.rcpath = Path.home() / Path(".smslibrc.toml")
        optpath = os.getenv("SMSLIBRC")
        if optpath:
            self.rcpath = Path(optpath)
        if self.rcpath.exists():
            print("exists")
            self.rcconfig = tomllib.loads(self.rcpath.read_text(encoding="utf-8"))
        else:
            self.rcconfig = {"senders": dict(), "receivers": dict()}

    def cli(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("message")
        parser.add_argument("--sender")
        parser.add_argument("--receiver")
        parser.add_argument("--email")
        parser.add_argument("--password")
        parser.add_argument("--smtp-server")
        parser.add_argument("--port", default=587)
        parser.add_argument("--phone-number")
        parser.add_argument("--provider")
        parser.add_argument("--confirm", action="store_true")
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
            sender_password = getpass.getpass(prompt="Enter the sender's email password: ")
        while not sender_smtp_server:
            sender_smtp_server = input("Enter the sender's SMTP server: ")
        sender = Sender(sender_email, sender_password, sender_smtp_server, sender_port)
        sender.check_credentials()
        receiver = None
        if not receiver_email:
            while not receiver_phone_number:
                receiver_phone_number = input("Enter the receiver's phone number: ")
            if not receiver_provider:
                print(f"Available providers: {', '.join(Receiver.GATEWAYS.keys())}")
            while not receiver_provider:
                receiver_provider = input("Enter the receiver's phone service provider: ")
            receiver = Receiver(receiver_phone_number, receiver_provider)
        else:
            receiver = Receiver(None, None, email=receiver_email)
        sender.send_message(args.message, receiver)
        if args.confirm:
            print("Message sent!")

def main():
    Notifier().cli()
