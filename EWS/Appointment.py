from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SendAppointment:
    subject: str
    requiredAtendees: str
    optionalAtendees: str
    body: str
    startTime: datetime
    endTime: datetime

    
    def __init__(self, requiredAttendees:str, startTime:datetime, endTime:datetime = None, subject:str ="", optionalAttendees:str = "", 
        body:str = ""):
        if not requiredAttendees and not optionalAttendees:
            raise ValueError("Appointment must have atendees")
        if not startTime:
            raise ValueError("Appointment must have start time")
        self.requiredAttendees = "" if not requiredAttendees else requiredAttendees 
        self.optionalAttendees = "" if not optionalAttendees else optionalAttendees
        self.subject = subject
        self.body = body
        self.startTime = startTime
        if not endTime:
            self.endTime = startTime + timedelta(minutes=30) # Set Default duration of 30 minutes
        else: 
            self.endTime = endTime
