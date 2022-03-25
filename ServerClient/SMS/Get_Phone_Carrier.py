#pip install phonenumbers
import phonenumbers
from phonenumbers import carrier



mobileno = input("Enter mobile number with country code: ")
mobileno=phonenumbers.parse(mobileno, "US")
print(mobileno)
carrier_name = carrier.name_for_valid_number(mobileno,"en")
print("the carrier is " + str(carrier_name))
print("Valid mobile number: ",phonenumbers.is_valid_number(mobileno))

