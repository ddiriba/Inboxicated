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

    try:
        data = json.loads(returned_text)
        carrier = str(data["carrier"]["name"])
        return carrier
    except:
        return 'NotFound'
    
if __name__ == '__main__':
    #clean_up()#run after

    phone_number_list = ['7754008918', '7753575103', '7025170712', 
                         '7025334544', '7756227397', '7753387648', 
                         '7753134694', '7023321538', '2068181776']


    name_list = ['Dawit', 'Carli', 'Dani', 
                 'Jake', 'Andrew', 'Julia' , 
                 'John', 'Jervyn', 'Julia Coach']

    carrier_list = []
    for i in phone_number_list:
        carrier_list.append(getCarrier(i))

    for j in range(len(phone_number_list)):
        print(name_list[j] + ' : ' + phone_number_list[j] + ' : ' + carrier_list[j])