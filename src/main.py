import requests 
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
auth_url="https://www.fitbit.com/oauth2/authorize"
token_url="https://api.fitbit.com/oauth2/token"
redirect_url = "http://localhost:8000"

params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_url": redirect_url,
    "scope": "activity",
}

# def print_url(r, *args, **kwargs):
#    print(r.url)
#    return

# res = requests.get(f"{auth_url}", params=params, hooks={'response': print_url})

res = requests.get(f"{auth_url}", params=params) 

print(res.content)