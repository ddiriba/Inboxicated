import requests
import json
def getCarrier(number):
    url = 'https://api.telnyx.com/v1/phone_number/1' + number
    html = requests.get(url).text
    data = json.loads(html)
    carrier = data["carrier"]["name"]
    return carrier

print(getCarrier('7754008918'))