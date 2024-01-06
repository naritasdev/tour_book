"""email delivery app"""

from dotenv import load_dotenv
import os
load_dotenv()
import requests
import json

SMTP_API_KEY= os.getenv("SMTP_API_KEY")
SMTP_URL=os.getenv("SMTP_URL")

def send_email(**emails):
    """

    Parameters
    ----------
    **emails : dict
        A dictionary with tuples or list of tuples.  Each tuple represent
        a name,email pair.  
        

    Returns
    -------
    response: json
        Response of the API request to delivery emails to tour stakeholders.

    """

    sender_dict = {"name":str(emails['sender'][0]), "email":str(emails['sender'][1])}
    reply_dict = {"name":str(emails['reply'][0]), "email":str(emails['reply'][1])}

    def receivers(email_list):
        receiver_dicts = []
        receiver_dict = {}
        for receiver in email_list:
            receiver_dict.update({"name":str(receiver[0]), "email":str(receiver[1])})
            receiver_dicts.append(receiver_dict.copy())
        return receiver_dicts

    payload = '{"sender": ' + str(json.dumps(sender_dict)) \
    + ',"replyTo": ' + str(json.dumps(reply_dict)) \
    + ',"to":' + str(json.dumps(receivers(emails['to']))) \
    + ',"cc":'  + str(json.dumps(receivers(emails['cc']))) \
    + ',"bcc":' + str(json.dumps(receivers(emails['bcc']))) \
    + ',"htmlContent":"' + str(emails['htmlContent']) + '"' \
    + ',"textContent":" ' + str(emails['textContent']) + '"' \
    + ',"subject":"' + str(emails['subject']) + '"' \
    + ',"tags":' + str(emails['tags']) + '}'
    url= SMTP_URL    
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": SMTP_API_KEY
    }
    response = requests.post(url, json=json.loads(payload), headers=headers)
    return response.json()
