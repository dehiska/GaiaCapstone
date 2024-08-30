# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
import os


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




#import from snippets
from snippets import estimate_emissions, endpoints

class ActionCalculateEmissions(Action):

    def name(self) -> str:
        return "action_calculate_emissions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        # Get the activity slot
        activity = tracker.get_slot("activity")

        # Retrieve the relevant endpoint configuration for the activity
        endpoint = endpoints.get(activity)
        
        if not endpoint:
            dispatcher.utter_message(text=f"Sorry, I don't have data for the activity '{activity}'.")
            return []
        
        # Prepare parameters based on the slots and the required parameters for the activity
        parameters = {}
        for param_name, param_type in endpoint["parameters"].items():
            slot_value = tracker.get_slot(param_name)
            if slot_value is not None:
                # Ensure parameters are correctly formatted based on expected types
                if param_type == "number":
                    try:
                        slot_value = float(slot_value)
                    except ValueError:
                        dispatcher.utter_message(text=f"Invalid value for {param_name}. Please provide a valid number.")
                        return []
                parameters[param_name] = slot_value
        
        # Call the estimate_emissions function
        emissions_result = estimate_emissions(endpoint["activity_id"], parameters)

        # Dispatch the result to the user
        if 'error' in emissions_result:
            dispatcher.utter_message(text=f"Error: {emissions_result['message']}")
        else:
            emission_value = emissions_result.get("co2e", "N/A")
            dispatcher.utter_message(text=f"The estimated emissions for {activity} are {emission_value} kg CO2e.")

        return []