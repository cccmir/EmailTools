# pylint: disable-msg=E0611

import os
import random
from datetime import datetime, timedelta

from exchangelib import Credentials, Configuration, Account, Message, Mailbox, EWSDateTime, CalendarItem
from exchangelib.queryset import DoesNotExist

from .Email import SendEmail
from .Appointment import SendAppointment


class EwsApi:
    def __init__(self, email, password):
        self.credentials = Credentials(username=email, password=password)
        config = Configuration(credentials=self.credentials, server='outlook.office365.com', has_ssl=True)
        self.account = Account(primary_smtp_address=email, credentials=self.credentials, autodiscover=False,
                               config=config)

    def sendMail(self, sendEmail: SendEmail) -> bool:
        to_recipients = []
        cc_recipients = []
        bcc_recipients = []
        if not sendEmail.to and not sendEmail.cc:
            raise Exception('Trying to send email without recepients')

        for rec in sendEmail.to.split(';'):
            if rec == "":
                continue
            to_recipients.append(Mailbox(email_address=rec))

        for rec in sendEmail.cc.split(';'):
            if rec == "":
                continue
            cc_recipients.append(Mailbox(email_address=rec))

        for rec in sendEmail.bcc.split(';'):
            if rec == "":
                continue
            bcc_recipients.append(Mailbox(email_address=rec))

        Message(account=self.account, subject=sendEmail.subject, body=sendEmail.body, to_recipients=to_recipients, 
                cc_recipients=cc_recipients, bcc_recipients=bcc_recipients).send_and_save()

    def createAppointment(self, sendAppointment: SendAppointment ):

        required_recipients = []
        optional_recipients = []

        for attendee in sendAppointment.requiredAttendees.split(';'):
            if attendee == "":
                continue
            required_recipients.append(attendee)

        for attendee in sendAppointment.optionalAttendees.split(';'):
            if attendee == "":
                continue
            optional_recipients.append(attendee)

        calendar_item = CalendarItem(
            account=self.account, folder=self.account.calendar,
            start=self.account.default_timezone.localize(EWSDateTime.from_datetime(sendAppointment.startTime)),
            end=self.account.default_timezone.localize(EWSDateTime.from_datetime(sendAppointment.endTime)),
            subject=sendAppointment.subject, body=sendAppointment.body, required_attendees=required_recipients, optional_attendees=optional_recipients)
        
        # 'SendToNone', 'SendOnlyToAll', 'SendToAllAndSaveCopy
        calendar_item.save(send_meeting_invitations='SendToAllAndSaveCopy')
