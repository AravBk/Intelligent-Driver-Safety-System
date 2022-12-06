import requests
import geocoder
g = geocoder.ip('me')

lati = 43.0029759
long = -78.7876123

TOKEN = "5880592883:AAG3gvM6dwN45TGkrx9hHvIHKebdrsJ9lnw"
# Aravind
chat_id1 = "333341036" 

#Rithvik
chat_id2 = "891482248"

# Oviyaa
chat_id3 = "1059399523"

message = "Hello, This is Driver Safety Bot"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
loc = f"https://api.telegram.org/bot{TOKEN}/sendlocation?chat_id={chat_id}&latitude={lati}&longitude={long}"
print(requests.get(url).json()) # this sends the message
print(requests.get(loc).json()) 

