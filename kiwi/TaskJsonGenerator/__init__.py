from celery import Celery
from celery.schedules import crontab
import json
import requests

#This is the url from redis
BROKER_URL = 'redis://localhost:6379/0'
# ID App from openexchangerates.org
ID_APP = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx'
#Inicialize Celery as app
app = Celery('TaskJsonGenerator', broker=BROKER_URL)

#This will be the function who generates the JSON file
@app.task
def JsonGenerator():
    print('Generating new currencies.....')
    data = {}
    #We used openexchangerates API, you must pay if you want to have all the combinations with all the currencies, so
    #I used USD dolars as a factor of change, and then we don't need to pay for the services.
    response = json.loads(requests.get("https://openexchangerates.org/api/latest.json?app_id="+ID_APP).text)     
    USDEUR = response["rates"]["EUR"]
    USDCZK = response["rates"]["CZK"]
    USDPLN = response["rates"]["PLN"]
    data['CurrenciesExchanges'] = []
    data['CurrenciesExchanges'].append({
        "name": "USD",
        "ValueToEuro": USDEUR,
        "ValueToKoruna": USDCZK,
        "ValueToZloty": USDPLN,
        "ValueToDollar": 1
    })
    data['CurrenciesExchanges'].append({
        "name": "CZK",
        "ValueToEuro": USDEUR/USDCZK,
        "ValueToKoruna": 1,
        "ValueToZloty": USDPLN/USDCZK,
        "ValueToDollar": 1/USDCZK
    })
    data['CurrenciesExchanges'].append({
        "name": "PLN",
        "ValueToEuro": USDEUR/USDPLN,
        "ValueToKoruna": USDCZK/USDPLN,
        "ValueToZloty": 1,
        "ValueToDollar": 1/USDPLN
    })
    data['CurrenciesExchanges'].append({
        "name": "EUR",
        "ValueToEuro": 1,
        "ValueToKoruna": USDCZK/USDEUR,
        "ValueToZloty": USDPLN/USDEUR,
        "ValueToDollar": 1/USDEUR
    })    
    #We create the file Api/JsonCurrencies.json if does not exist with all the currencies exchanges
    with open('Api/JsonCurrencies.json', 'w+') as outfile:
        json.dump(data, outfile)

#Here we configure the celery to execute the function every day 
app.conf.beat_schedule = {
    # Executes every day morning at 12:00
    'execute-every-day-12:00': {
        'task': 'TaskJsonGenerator.JsonGenerator',
        'schedule': crontab(minute='0', hour='12', day_of_week='*')
    },
}
#We use GMT+2 timezone
app.conf.timezone = 'Europe/Madrid'