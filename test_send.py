import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TG_BOT_TOKEN")
chat = os.getenv("TG_CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"
requests.post(url, data={"chat_id": chat, "text": "Bot funcionando!"})
