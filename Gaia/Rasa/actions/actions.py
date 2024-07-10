# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
class ActionHelloWorld(Action):
#
    def name(self) -> Text:
        return "action_hello_world"
#
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
        dispatcher.utter_message(text="Hello World!")
#
        return []
#npm install @openapitools/openapi-generator-cli -g
#pip install requests

#import requests
#CARBON_INTERFACE_API_KEY = 'CzQS7w8a6WBAGToUjk5Q'

#def get_car_emissions(miles):
#   url = "https://www.carboninterface.com/api/v1/estimates"
#    headers = {
#        'Authorization': f'Bearer {CARBON_INTERFACE_API_KEY}',
 #       'Content-Type': 'application/json'
  #  }
   # data = {
    #    "type": "vehicle",
     #   "distance_unit": "mi",
      #  "distance_value": miles,
       # "vehicle_model_id": "2b7bbf40-79ec-4567-9c6b-9f0e745d7e2d"  # average gasoline car
   # }
    #response = requests.post(url, headers=headers, json=data)
    #emissions = response.json()['data']['attributes']['carbon_kg']
    #return emissions