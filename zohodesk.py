import os
import requests
from dotenv import load_dotenv
load_dotenv()

ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")
ZOHO_DEPT_ID = os.getenv("ZOHO_DEPT_ID")

def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json().get("access_token")

def create_ticket(user_name, subject, description):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "orgId": ZOHO_ORG_ID,
        "Content-Type": "application/json"
    }

    data = {
        "subject": subject,
        "departmentId": ZOHO_DEPT_ID,
        "description": description,
        "contact": {"lastName": user_name}
    }

    r = requests.post("https://desk.zoho.com/api/v1/tickets", headers=headers, json=data)
    r.raise_for_status()
    return r.json().get("ticketNumber")
