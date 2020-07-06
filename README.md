# kiwi
required packages:

pip3 install celery
pip3 install -U redis
pip3 install Flask
pip3 install requests

The project have 3 parts: External query automate task, REST API server and a test web

Part 1) TaskjsonGenerator, allows to create the json file into /Api to get all de currency exchanges. It works with Celery 
and redis every day at 12:00 makes a API query to openexchangerates.org, you need to put your API key!!!! to get all USD echange rate currencies and 
then stores into Api/jsonCurrencies.json. The way to start the schedule task is going to the project path using the console
prompt and execute:

# celery -A TaskJsonGenerator worker -B -l info

part 2) Api, It works with flask framework, and generates the API with the right format for the currency exchanges  
Czech koruna, Euro, Polish złoty and US dollar. it works on the port 5000. Once you execute the python script, the flask
will automatically start on the port 5000, the way to check if it works put in to the browser:

http://localhost:5000/currency/eur

part 3) Finally I created a simple test webside with jquery to test the APPI, it uses the same flask but diferent path:

http://localhost:5000/test
