
from EWS import EwsApi, SendAppointment, SendEmail
from RandomQuotes import RandomQuotesGenerator
from configuration import Configuration, ItemType

from datetime import datetime, timedelta
import logging
import random
import getpass
import json
import argparse

log = logging.getLogger(__name__)
ewsApi = None

def initEwsApi(userName, password):
    global ewsApi
    ewsApi = EwsApi(userName, password)

def SendRandomAppointments(required:str, optional:str=None, cnt:int = 1):
    if not ewsApi:
        raise Exception("EWSAPI Is not initialized")

    log.debug("Sending random Appointment")
    qts = RandomQuotesGenerator.getRandomQuotes(cnt)
    for i in range(cnt):
        log.debug("sending {} email with quote title: {}".format(i, qts[i].title))
        sendApp = SendAppointment(requiredAttendees=required, optionalAttendees=optional, subject='random quote by {}'.format(qts[i].title), 
        startTime = datetime.now() + timedelta(hours=i), body= qts[i].content)
        ewsApi.createAppointment(sendApp)

def SendRandomEmails(to:str, cc:str = None, bcc=None, cnt:int = 1):
    if not ewsApi:
        raise Exception("EWSAPI Is not initialized")
  
    log.debug("Getting random quotes")
    qts = RandomQuotesGenerator.getRandomQuotes(cnt)
    for i in range(cnt):
        sendEmail = SendEmail(to=to,cc=cc, bcc=bcc, subject='random quote by {}'.format(qts[i].title), body=qts[i].content)
        log.debug("sending {} email with quote {}".format(i, qts[i].title))
        ewsApi.sendMail(sendEmail)


def getItemType() -> ItemType:
    print("Choose your item type")
    print("1. Email")
    print("2. Appointment")
    itemType = None
    tryCount = 0
    while not itemType: 
        if tryCount > 3:
            print("To many tryouts")
            exit(0)
        try:
            itemType = input("Please choos item type: (Email)")
            if not itemType:
                itemType = 1
            itemType = int(itemType)
        except:
            log.exception("Wrong item type")
            itemType = None
            tryCount += 1
    return ItemType(itemType)
 
def collectItemDataAndSend(itemType: ItemType):
    # Collect Shared:
    if itemType == ItemType.Email:
        to = input('To recepeints (seperated by ;): ')
        cc = input('Cc recepeints (seperated by ;): ')
        bcc = input('Bcc recepeints (seperated by ;): ')
        cnt = int(input("How many items to send?"))
        SendRandomEmails(to, cc, bcc, cnt)
    elif itemType == ItemType.APPOINTMET:
        req = input('Required Attendees (seperated by ;)')
        opt = input('Optional Attendees (seperated by ;)')
        cnt = int(input('How many items to send?'))
        SendRandomAppointments(req, opt, cnt)
    
    else:
        raise Exception("failed to recognize item type")


def SendFromConfiguration(config: Configuration):
    if config.itemType == ItemType.Email:
        SendRandomEmails(config.to, config.cc, config.bcc, config.count)
    elif config.itemType == ItemType.APPOINTMET:
        SendRandomAppointments(config.required, config.optional, config.count )
    else:
        raise Exception("failed to recognize item type")

def main(configurationFilePath:str = None):
    if not configurationFilePath:
        print('Fill to username and password for the sending account')
        user = input('Username:')
        password = getpass.getpass(prompt='Password:')
        
        initEwsApi(user, password) # Async?
        itemType = getItemType()
        collectItemDataAndSend(itemType)
        print("Done.")
    else:
        with open(configurationFilePath, "r", encoding='UTF-8') as configFile: 
            try:
                config = Configuration(json.load(configFile))
            except:
                log.exception("Failed to load config from path: {}".format(configurationFilePath))
                exit(0)

        if not config:
            log.error("Config object is empty")
            return
        initEwsApi(config.sender, config.password)
        SendFromConfiguration(config)
   
if __name__ == "__main__":
    logging.basicConfig()
    parser = argparse.ArgumentParser(description='Random email or appointment generator')
    parser.add_argument('-c', help='path to the configuration file', required=False, type=str, default=None)
    args = parser.parse_args()
    main(args.c)
    