from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os
from snippets import endpoints, estimate_emissions



distance_unit_mapping = {
    "mi": "mi",
    "miles": "mi",
    "mile": "mi",
    "km": "km",
    "km": "km",
    "kilometers": "km",
    "kilometer": "km",
    "kilmeter": "km",
    "klometer": "km",
    "kilomter": "km",
    "kilometr": "km",
    "meter": "m",
    "metrs" : "m",
    "mters" : "m",
    "m": "m",
    "meters": "m",
    "ft": "ft",
    "foot":"ft",
    "fet":"ft",
    "feet": "ft",
    "nmi": "nmi",
    "natical miles": "nmi",
    "nautical mile": "nmi",
    "nm" : "nmi",
    "nauticl" : "nmi",
    "nautical miles": "nmi"
}

money_unit_mapping = {
    "USD": "USD",
    "us dollar": "USD",
    "dollar": "USD",
    "CAD" : "CAD",
    "Canadian dollars": "CAD",
    "canadian dollars" : "CAD",
    "Australian Dollars" : "AUD",
    "Australian dollar" : "AUD",
    "USD": "usd",
    "EUR": "eur",
    "USD": "$",
    "EUR": "€",
    "usd": "USD",
    "dollars": "USD",
    "EUR": "EUR",
    "eur": "EUR",
    "euros": "EUR",
}

class Action_Calculate_Emissions(Action):

    def name(self) -> str:
        return "action_calculate_emissions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Get the activity slot
        activity = tracker.get_slot("activity")
        available_activities = "\n".join([f"{i+1}. {act}" for i, act in enumerate(endpoints.keys())])

        if activity is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify an activity from our list?")
            dispatcher.utter_message(
                text=f"Here are the available activities:\n{available_activities}"
            )
            return []

        # Retrieve the relevant endpoint configuration for the activity
        endpoint = endpoints.get(activity)

        if not endpoint:
            dispatcher.utter_message(
                text=f"Sorry, I don't have data for the activity '{activity}'. Here are the available activities:\n{available_activities}"
            )
            return []

        # Prepare parameters based on the slots and the required parameters for the activity
        parameters = {}
        missing_params = []

        # Validation and mapping for parameters
        valid_distance_units = set(distance_unit_mapping.values())

        # Get slots for distance and distance_unit
        distance = tracker.get_slot("distance")
        distance_unit = tracker.get_slot("distance_unit")

        # First check if distance is missing, if so, prompt for it
        if distance is None:
            dispatcher.utter_message(text="Please provide the distance.")
            return []

        # After distance is provided, check if distance_unit is missing
        if distance_unit is None:
            dispatcher.utter_message(text="Please provide the unit of distance (e.g., miles, kilometers).")
            return []

        # Ensure the unit is valid
        standardized_unit = distance_unit_mapping.get(distance_unit.lower())
        if standardized_unit not in valid_distance_units:
            dispatcher.utter_message(text=f"Invalid distance unit '{distance_unit}'. Please use one of the following: {', '.join(valid_distance_units)}.")
            return []

        parameters["distance"] = distance
        parameters["distance_unit"] = standardized_unit

        # Call the estimate_emissions function if all required parameters are present
        emissions_result = estimate_emissions(activity_id=endpoint["activity_id"], parameters=parameters)

        # Dispatch the result to the user
        if 'error' in emissions_result:
            dispatcher.utter_message(text=f"Error: {emissions_result['message']}")
        else:
            emission_value = emissions_result.get("co2e", "N/A")
            dispatcher.utter_message(text=f"The estimated emissions for {activity} are {emission_value} kg CO2e.")

        return []


"""" John's code before Denis touched it to try to fix the hallucinations
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os

'''
class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[EventType]:
        # Start a session
        events = [SessionStarted()]
        
        # Greet the user when the session starts
        dispatcher.utter_message(text="Hello! How can I help you today? Here are a few things I can do:\n1. Calculate emissions")
        
        # Ask user to choose an option
        dispatcher.utter_message(text="Please type 'Calculate emissions' to get started.")
        
        events.append(ActionExecuted("action_listen"))
        return events
'''

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


distance_unit_mapping = {
    "mi": "mi",
    "miles": "mi",
    "mile": "mi",
    "km": "km",
    "km": "km",
    "kilometers": "km",
    "kilometer": "km",
    "kilmeter": "km",
    "klometer": "km",
    "kilomter": "km",
    "kilometr": "km",
    "meter": "m",
    "metrs" : "m",
    "mters" : "m",
    "m": "m",
    "meters": "m",
    "ft": "ft",
    "foot":"ft",
    "fet":"ft",
    "feet": "ft",
    "nmi": "nmi",
    "natical miles": "nmi",
    "nautical mile": "nmi",
    "nm" : "nmi",
    "nauticl" : "nmi",
    "nautical miles": "nmi"
}

money_unit_mapping = {
    "USD": "USD",
    "us dollar": "USD",
    "dollar": "USD",
    "CAD" : "CAD",
    "Canadian dollars": "CAD",
    "canadian dollars" : "CAD",
    "Australian Dollars" : "AUD",
    "Australian dollar" : "AUD",
    "USD": "usd",
    "EUR": "eur",
    "USD": "$",
    "EUR": "€",
    "usd": "USD",
    "dollars": "USD",
    "EUR": "EUR",
    "eur": "EUR",
    "euros": "EUR",
}

#import from snippets
endpointsfrom snippets import estimate_emissions, 

class ActionCalculateEmissions(Action):

    def name(self) -> str:
        return "action_calculate_emissions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Get the activity slot
        activity = tracker.get_slot("activity")
        available_activities = "\n".join([f"{i+1}. {act}" for i, act in enumerate(endpoints.keys())])

        if activity is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify an activity from our list?")
            dispatcher.utter_message(
                text=f"Here are the available activities:\n{available_activities}"
            )
            return []

        # Retrieve the relevant endpoint configuration for the activity
        endpoint = endpoints.get(activity)

        if not endpoint:
            # Create a numbered list of available activities
            dispatcher.utter_message(
                text=f"Sorry, I don't have data for the activity '{activity}'. Here are the available activities:\n{available_activities}"
            )
            return []

        # Prepare parameters based on the slots and the required parameters for the activity
        parameters = {}
        missing_params = []

        # Validation and mapping for parameters
        valid_distance_units = set(distance_unit_mapping.values())
        valid_money_units = set(money_unit_mapping.values())

        for param_name, param_type in endpoint["parameters"].items():
            slot_value = tracker.get_slot(param_name)

            if slot_value is None:
                missing_params.append(param_name)
            else:
                if param_type == "number":
                    try:
                        slot_value = float(slot_value)
                    except ValueError:
                        dispatcher.utter_message(text=f"Invalid value for {param_name}. Please provide a valid number.")
                        return []
                elif param_name == "distance_unit":
                    standardized_unit = distance_unit_mapping.get(slot_value.lower())
                    if standardized_unit not in valid_distance_units:
                        dispatcher.utter_message(text=f"Invalid distance unit '{slot_value}'. Please use one of the following: {', '.join(valid_distance_units)}.")
                        return []
                    parameters[param_name] = standardized_unit
                elif param_name == "money_unit":
                    standardized_unit = money_unit_mapping.get(slot_value.lower())
                    if standardized_unit not in valid_money_units:
                        dispatcher.utter_message(text=f"Invalid money unit '{slot_value}'. Please use one of the following: {', '.join(valid_money_units)}.")
                        return []
                    parameters[param_name] = standardized_unit

                parameters[param_name] = slot_value

        # If there are missing parameters, prompt the user for them and stop the action
        if missing_params:
            for param in missing_params:
                if param in ["money", "money_unit"]:
                    dispatcher.utter_message(text="Please provide the amount and the unit of money.")
                elif param in ["distance", "distance_unit"]:
                    dispatcher.utter_message(text="Please provide the distance and the unit of distance.")
                else:
                    dispatcher.utter_message(text=f"Missing parameter: {param}. Please provide it.")
            return []

        # Call the estimate_emissions function if all required parameters are present
        emissions_result = estimate_emissions(endpoint["activity_id"], parameters)

        # Dispatch the result to the user
        if 'error' in emissions_result:
            dispatcher.utter_message(text=f"Error: {emissions_result['message']}")
        else:
            emission_value = emissions_result.get("co2e", "N/A")
            dispatcher.utter_message(text=f"The estimated emissions for {activity} are {emission_value} kg CO2e.")

        return []


"""