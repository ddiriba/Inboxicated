import email, smtplib, ssl
from SMS.providers import PROVIDERS
import requests
import urllib3
import time
import json

def getCarrier(number):
    carrier = ''
    returned_status = 429
    returned_text = ''
    
    #too many requests status code
    while returned_status == 429: 
        url = 'https://api.telnyx.com/v1/phone_number/1' + number
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        request_returned = requests.get(url, verify = False)
        returned_text = request_returned.text
        returned_status = request_returned.status_code
        time.sleep(2) #wait 2 seconds
    carrier = ''
    try:
        data = json.loads(returned_text)
        carrier = str(data["carrier"]["name"])
    except:
        carrier = ''
        
    formatted_carrier = ''

    if "T-MOBILE" in carrier:
        formatted_carrier = "T-Mobile"
    elif "VERIZON" in carrier:
        formatted_carrier = "Verizon"
    elif "NEW CINGULAR" in carrier:
        formatted_carrier = "AT&T"
    else:
        print('Bizzare carrier found')

    return formatted_carrier


def send_sms_via_email(number, message, provider):

    sender_email = "inboxicatedteam@gmail.com"
    email_password = "tvytfdhryqkafpys" #very very safe
    smtp_server = "smtp.gmail.com"
    subject = "Inboxicated Notifcation"
    smtp_port= 465
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
    print(receiver_email)

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, 
                            smtp_port, 
                            context=ssl.create_default_context()
                            ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def send_too_many_attempts_alert(number):
    provider = getCarrier(number)
    message = "A user has tried to open the box way too many times, please assist user at the box!"

    if provider == '':
        print('Cannot find provider for phone')
        return False
    else:
        send_sms_via_email(number, message, provider)
        return True

def send_override_request(number):
    provider = getCarrier(number)
    message = "A user requires your assistance, please go to the box to assist!"
    if provider == '':
        print('Cannot find provider for phone')
        return False
    else:
        send_sms_via_email(number, message, provider)
        return True


if __name__ == "__main__":
    send_too_many_attempts_alert("7754008918")
    send_override_request("7754008918")