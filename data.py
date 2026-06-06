import os
import requests
import base64
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

CLIENT_ID     = os.getenv("RTE_CLIENT_ID")
CLIENT_SECRET = os.getenv("RTE_CLIENT_SECRET")

def get_token():
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    response = requests.post(
        "https://digital.iservices.rte-france.com/token/oauth/",
        headers={"Authorization": f"Basic {credentials}"},
    )
    return response.json()["access_token"]

def get_day_ahead_prices(start_date, end_date):
    token = get_token()
    response = requests.get(
        "https://digital.iservices.rte-france.com/open_api/wholesale_market/v3/france_power_exchanges",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "start_date": f"{start_date}T00:00:00+02:00",
            "end_date": f"{end_date}T00:00:00+02:00",
        }
    )
    data =  response.json()
    values = data['france_power_exchanges'][0]["values"]
    df = pd.DataFrame(values)
    df["start_date"] = pd.to_datetime(df["start_date"])
    return df