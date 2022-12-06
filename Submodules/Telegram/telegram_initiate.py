# Python Code to Initite Connection with Telegram Bot using BotFather

import requests
TOKEN = "5880592883:AAG3gvM6dwN45TGkrx9hHvIHKebdrsJ9lnw"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
print(requests.get(url).json())