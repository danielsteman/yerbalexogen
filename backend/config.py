from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
TOKEN_URL = "https://api.fitbit.com/oauth2/token"
REDIRECT_URL = "http://localhost:8000"
SCOPE = "activity heartrate"

BASE_URL = "https://api.fitbit.com"


def GET_HRV_SUMMARY_BY_DATE(user_id, date):
    return f"{BASE_URL}/1/user/{user_id}/hrv/date/{date}.json"
