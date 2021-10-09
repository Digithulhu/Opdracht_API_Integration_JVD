# Standaard imports die we nodig hebben om 1. een correcte url op te bouwen en 
# 2. de informatie die we terugkrijgen van onze request te kunnen vertalen
import urllib.parse
import requests
# datetime module import omdat we deze kunnen gebruiken voor de timestamp variabele
from datetime import datetime
# ik heb geprobeerd met de voorgestelde base64 module import te werken maar jammergenoeg na lang troubleshooten
# voldoet deze niet, ipdv maak ik gebruik van de hashlib module voor de hash parameter in de request url 
# en is alle base64 code in commentaar gezet
# import base64
import hashlib

# We moeten een timestamp meegeven om te voldoen aan de voorwaarden van de API request
ts = datetime.today().strftime('%d%m%Y')

# Dit is de public API key
publicKey = "44cf8afd63d3c8a985e8df444822b5cf"

print("Hello! What Marvel universe character would you like to search information on?")

while True:
    try:
        # Hier geven we onze private API key in
        privateKey = input("Before we can start, we'll need your private key (Type quit or q to stop): ")
        if privateKey == "quit" or privateKey == "q":
                break

        toBeHashed = (ts+privateKey+publicKey) #.encode('UTF-8')

        # Nu hashen we deze informatie voor in onze request url later
        # paramHash = base64.b32hexencode(toBeHashed)
        paramHash = hashlib.md5(toBeHashed.encode('UTF-8')).hexdigest()
        
        while True:
            # deze zoekfunctie maakt gebruik van de "namestartswith" parameter om makkelijker resultaten weer te geven,
            # je zal er dus meer krijgen, de eigenlijke "name" parameter moet 100% overeenkomen met een naam,
            # je zal geen resultaten krijgen bij een search op "spiderman" omdat de naam anders is in de database
            # in dit geval als je "spider" typt kan je hem wel terugvinden uit de resultaten -> wat ik denk beter is
            paramName = input("Character name (Type quit or q to stop): ")
            if paramName == "quit" or paramName == "q":
                break
            
            # Hier volgt het samenstellen van de request URL
            stringURL = "https://gateway.marvel.com:443/v1/public/characters?" + urllib.parse.urlencode({"nameStartsWith":paramName, "ts":ts, "apikey":publicKey, "hash":paramHash})

            # We slaan de data die we binnekrijgen op in een variabele
            json_data = requests.get(stringURL).json()

            # In geval dat er (geen) resultaten zijn voor een naam kunnen we adhv de volgende variabele
            # in een if, dus wel of niet, geschikte antwoorden geven
            json_status = json_data['data']['total']
            if json_status > 0:
                print("API Status (number of results): " + str(json_status) + " = A successful call.\n")
                print ("{:<60} {:<50} {:<7}".format('Matching character names','Date of last entry','comics') + '\n')
                for item in json_data['data']['results']:
                    print ("{:<60} {:<50} {:<7}".format(item['name'], item['modified'], item['comics']['available']))
                print('\n' + json_data['attributionText'])
            else:
                print("API Status (number of results): " + str(json_status) + " = A successful call.\n")
                print("As you can tell by the number of results, there were no matches for this character name.\nTry searching for a part of the start of the name if you are certain this is a Marvel universe character.")
    except KeyError:
        print("The private key you provided was probably wrong, please try again with a valid private key.")
    
