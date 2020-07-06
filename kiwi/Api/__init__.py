# We will use the framework flask to develop our REST API
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import json
import requests
#Inicialize flask 
app = Flask(__name__)
api = Api(app)

#We need to read all the exchange rates from the file JsonCurrencies.json previously created by the celery task
with open('JsonCurrencies.json') as json_file:
    data = json.load(json_file)
    currencies = data['CurrenciesExchanges']
    
# We will use http response code: 200 OK and 404 Not Found
# We just need to give information not to delete or add or modify, so i just need to implement the GET resource
class excahnge(Resource):
    def get(self, CurrencyName):
        #Transform to uppercase in any case
        CurrencyName = CurrencyName.upper()
        for currency in currencies:
            if(CurrencyName == currency["name"]):
                #If its right:
                return currency, 200
        #If its wrong:
        return "Currency --> "+CurrencyName+" <-- not found!!!!!!!!", 404
    
#URL format will be for example http://localhost/currency/eur
api.add_resource(excahnge, "/currency/<string:CurrencyName>")

@app.route("/test")
def test():
    return render_template('TestWebCurrency.html')

app.run(debug=True)