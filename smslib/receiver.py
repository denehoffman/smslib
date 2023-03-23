import re as _re

class Receiver:
    GATEWAYS = {
            'verizon': 'vtext.com',
            'at&t': 'txt.att.net',
            'att': 'txt.att.net',
            'tmobile': 'tmomail.net',
            'sprint': 'messaging.sprintpcs.com',
            'boost': 'myboostmobile.com'
            }

    def __init__(self, phone_number, service_provider, email=None):
        self._phone_number = None
        self.phone_number = self.format_phone_number(phone_number)
        self.service_provider = service_provider
        if email is None:
            self.email = self.construct_email()
        else:
            self.email = email # option to use custom email, set phone_number = None

    @property
    def phone_number(self):
        return self._phone_number
    
    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = self.format_phone_number(value)

    def format_phone_number(self, phone_number):
        if phone_number is None:
            return None
        # Regex to match common US phone patterns
        phone_regex = _re.compile(r'(?:\+1-)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})')
        match = phone_regex.search(phone_number)
        if match:
            return match.group(1) + match.group(2) + match.group(3)
        else:
            print("Invalid phone number: {phone_number}")
            return None

    def construct_email(self):
        if not self.service_provider in Receiver.GATEWAYS.keys():
            raise ValueError("Invalid service provider")
        return f"{self.phone_number}@{Receiver.GATEWAYS[self.service_provider]}"
