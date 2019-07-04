# EmailTools
Tool for sending random emails and appointments from office 365.
this tool is created for testing purposes.

use the example configuration file or follow prompts from command line

### Configuration:
**sender**: The email account items are sent from
**password**: password to the sender account
**itemType**: type of item you want to send. 1 - Email, 2 - Appointment
**to**: to recepients, used with itemType 1
**cc**: cc recepients, used with itemType 1
**bcc**: bcc recepients, used with itemType 1
**required**: required attendees, used with itemType 2
**optional**: optional attendees, used with itemType 2
**count**: how many items send

Run with configuration: python SendRandomItem.py -c configFullPath

Run with prompt: python SendRandomItem.py 