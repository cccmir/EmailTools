from dataclasses import dataclass

@dataclass
class SendEmail:
    subject: str
    to: str
    cc: str
    bcc: str
    body: str
    
    def __init__(self, to:str, subject:str ="", cc:str = "", bcc:str="", body:str = ""):
        if not to and not cc and not bcc:
            raise ValueError("Email must have recepients")
        self.to = "" if not to else to
        self.subject = subject
        self.cc = "" if not cc else cc
        self.bcc = "" if not bcc else bcc
        self.body = body