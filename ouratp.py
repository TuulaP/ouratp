
from dotenv import load_dotenv
load_dotenv()


import json
import os
from datetime import datetime

from oura import OuraClient

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
#redirect_uri = os.environ.get("REDIRECT_URI")
#access_token = os.environ.get("TOKEN")


def get_self():
    pat = os.getenv("OURA_PAT")
    client = OuraClient(personal_access_token=pat)
    user_info = client.user_info()
    print(user_info)


def setEnvironment(envFile):
    basePath = os.path.dirname(os.path.abspath(__file__))
    fullPath = os.path.join(basePath, envFile)
    with open(fullPath) as file:
        env = json.load(file)
        os.environ["OURA_CLIENT_ID"] = env["client_id"]
        os.environ["OURA_CLIENT_SECRET"] = env["client_secret"]
        os.environ["OURA_ACCESS_TOKEN"] = env["access_token"]
        os.environ["OURA_REFRESH_TOKEN"] = env["refresh_token"]


def appendFile(filename, token_dict):

    basePath = os.path.dirname(os.path.abspath(__file__))
    fullPath = os.path.join(basePath, filename)
    with open(fullPath, "r+") as file:
        prev = json.load(file)
        curr = {
            "client_id": prev.pop("client_id"),
            "client_secret": prev.pop("client_secret"),
            "access_token": token_dict["access_token"],
            "refresh_token": token_dict["refresh_token"],
            "previous": json.dumps(prev),
        }
        file.seek(0)
        json.dump(curr, file)


def getOuraClient(envFile):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token = os.getenv("OURA_PAT")
    refresh_token = os.getenv("OURA_REFRESH_TOKEN")
    refresh_callback = lambda x: appendFile(envFile, x)

    print("AT", access_token)

    auth_client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_callback=refresh_callback,
    )

    return auth_client


if __name__ == "__main__":

    envFile = ".env" # "token.json"
    #setEnvironment(envFile)
    client = getOuraClient(envFile)
    #today = datetime.today()
    #sleep = client.sleep_summary(today)


    from datetime import date
    today = str("2022-05-01") # 2019-01-06, e,g, YYYY-MM-DD, or use whatever start/end date you want
    sleep = client.sleep_summary(start=today)

    # print(sleep)


    access_token = os.environ.get("OURA_PAT")

    from datetime import datetime, timedelta
    toay = datetime.today().strftime('%Y-%m-%d')   # '2021-01-26'
    
    yay =  datetime.today() - timedelta(days=1)
    yays = datetime.strftime(yay, '%Y-%m-%d')

    # print(toay, yay)

    import requests 
    url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
    params={ 
        'start_datetime': yays + 'T00:00:00-23:59', 
        'end_datetime': toay + 'T00:00:00-23:59' 
    }


    headers = { 
    'Authorization': 'Bearer ' + access_token, 
    }
    response = requests.request('GET', url, headers=headers, params=params) 

    #print(response.text)

    hrataj = json.loads(response.text)
    hrata = hrataj['data']

    # print(hrata)
    # if you need all events
    #for event in hrata:
    #    print(event['timestamp'], event['bpm'])

    # for getting latest HR number
    
    print(hrata[-1].get('timestamp'))
    print(hrata[-1].get('bpm'))


