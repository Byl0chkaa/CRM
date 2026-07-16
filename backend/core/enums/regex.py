from enum import Enum


class RegexPhoneNumber(Enum):
    PHONE_NUMBER = (
        r'(?=.*\+[0-9]{3}\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{4,5}$)',
        'Only ukrainian numbers allowed'
    )

    def __init__(self, pattern:str, msg:str ):
        self.pattern = pattern
        self.msg = msg
