from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os
from snippets import endpoints, estimate_emissions


# Mappings for units
distance_unit_mapping = {
    "mi": "mi",
    "miles": "mi",
    "mile": "mi",
    "km": "km",
    "km": "km",
    "kilometers": "km",
    "kilometer": "km",
    "meter": "m",
    "meters": "m",
    "ft": "ft",
    "foot": "ft",
    "fet": "ft",
    "feet": "ft",
    "nmi": "nmi",
    "nautical mile": "nmi",
    "nm": "nmi",
    "nautical": "nmi",
    "nautical miles": "nmi"
}

money_unit_mapping = {
    "USD": "USD",
    "us dollar": "USD",
    "dollar": "USD",
    "CAD": "CAD",
    "Canadian dollars": "CAD",
    "Australian Dollars": "AUD",
    "Australian dollar": "AUD",
    "usd": "USD",
    "dollars": "USD",
    "EUR": "EUR",
    "euros": "EUR",
}

# Emission factors for various activities
EMISSION_FACTORS = {
    "coal": 0.001,
    "petroleum": 0.00096,
    "natural_gas": 0.0004,
    "hydropower": 0.000019,
    "nuclear": 0.00000318,
    "car_gasoline": 0.0089,
    "car_diesel": 0.01018,
    "intercity_rail": 0.00014,
    "commuter_rail": 0.00017,
    "bus": 0.00006,
    "air_travel": 0.0002,
    "meat_diet": 1.3,
    "average_omnivore": 1.0,
    "vegetarian": 0.66,
    "vegan": 0.56,
}


class ActionCalculateEmissions(Action):

    def name(self) -> str:
        return "action_calculate_emissions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        activity = tracker.get_slot("activity")
        available_activities = "\n".join([f"{i + 1}. {act}" for i, act in enumerate(endpoints.keys())])

        if activity is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify an activity from our list?")
            dispatcher.utter_message(text=f"Here are the available activities:\n{available_activities}")
            return []

        endpoint = endpoints.get(activity)
        if not endpoint:
            dispatcher.utter_message(
                text=f"Sorry, I don't have data for the activity '{activity}'. Here are the available activities:\n{available_activities}")
            return []

        parameters = {}
        valid_distance_units = set(distance_unit_mapping.values())

        distance = tracker.get_slot("distance")
        distance_unit = tracker.get_slot("distance_unit")

        if distance is None:
            dispatcher.utter_message(text="Please provide the distance.")
            return []

        if distance_unit is None:
            dispatcher.utter_message(text="Please provide the unit of distance (e.g., miles, kilometers).")
            return []

        standardized_unit = distance_unit_mapping.get(distance_unit.lower())
        if standardized_unit not in valid_distance_units:
            dispatcher.utter_message(
                text=f"Invalid distance unit '{distance_unit}'. Please use one of the following: {', '.join(valid_distance_units)}.")
            return []

        parameters["distance"] = distance
        parameters["distance_unit"] = standardized_unit

        emissions_result = estimate_emissions(activity_id=endpoint["activity_id"], parameters=parameters)

        if 'error' in emissions_result:
            dispatcher.utter_message(text=f"Error: {emissions_result['message']}")
        else:
            emission_value = emissions_result.get("co2e", "N/A")
            dispatcher.utter_message(text=f"The estimated emissions for {activity} are {emission_value} kg CO2e.")

        return []

# Mappings for units
distance_unit_mapping = {
    "mi": "mi",
    "miles": "mi",
    "mile": "mi",
    "km": "km",
    "kilometers": "km",
    "kilometer": "km"
}
 
fuel_unit_mapping = {
    "gallons": "gallons",
    "gallon": "gallons",
    "liters": "liters",
    "liter": "liters"
}
 
# Conversion factors
LITERS_TO_GALLONS = 0.264172
KM_TO_MILES = 0.621371
 
# Emission factors
EMISSION_FACTORS = {
    "coal": 0.001,
    "petroleum": 0.00096,
    "natural gas": 0.0004,
    "hydropower": 0.000019,
    "nuclear": 0.00000318,
    "car gasoline": 0.0089,
    "car diesel": 0.01018,
    "air travel": 0.0002,
    "meat diet": 1.3,
    "average omnivore": 1.0,
    "vegetarian": 0.66,
    "vegan": 0.56,
}
 
class ActionLifestyleSurvey(Action):
    def name(self) -> str:
        return "action_lifestyle_survey"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        responses = {}
        # Retrieve slots and validate
        electricity_kwh = tracker.get_slot("electricity_kwh")
        energy_source = tracker.get_slot("energy_source")
        car_fuel_type = tracker.get_slot("car_fuel_type")
        car_miles = tracker.get_slot("car_miles")
        fuel_consumption = tracker.get_slot("fuel_consumption")
        short_flights = tracker.get_slot("short_flights")
        long_flights = tracker.get_slot("long_flights")
        diet = tracker.get_slot("diet")
        recycles = tracker.get_slot("recycles")

        # Error handling if slots are missing
        if not electricity_kwh:
            dispatcher.utter_message(text="Could you provide how many kWh of electricity you use per week?")
            return []
        if not energy_source:
            dispatcher.utter_message(text="What is your main energy source (coal, petroleum, natural gas, hydropower, nuclear)?")
            return []
        if not car_fuel_type:
            dispatcher.utter_message(text="What fuel does your car use (gasoline, gas, or diesel)?")
            return []
        if not car_miles:
            dispatcher.utter_message(text="How many miles or kilometers do you drive per week?")
            return []
        if not fuel_consumption:
            dispatcher.utter_message(text="How many gallons or liters of fuel does your car consume weekly?")
            return []
        if not short_flights:
            dispatcher.utter_message(text="How many short flights (under 3 hours) do you take per year?")
            return []
        if not long_flights:
            dispatcher.utter_message(text="How many long flights (over 3 hours) do you take per year?")
            return []
        if not diet:
            dispatcher.utter_message(text="What is your diet type (meat diet, average omnivore, vegetarian, vegan)?")
            return []
        if not recycles:
            dispatcher.utter_message(text="Do you recycle (yes or no)?")
            return []

        # Convert responses for emissions calculation
        responses["electricity_kwh"] = float(electricity_kwh) * 4  # Monthly kWh
        responses["energy_source"] = energy_source
        responses["car_fuel_type"] = car_fuel_type
        responses["car_miles"] = float(car_miles) * 4  # Monthly car distance
        responses["car_fuel_useage"] = float(fuel_consumption) * 4  # Monthly fuel consumption
        responses["short_flights"] = int(short_flights)
        responses["long_flights"] = int(long_flights)
        responses["diet"] = diet
        responses["recycles"] = recycles

        # Calculate emissions
        total_emissions = self.calculate_carbon_footprint(responses)

        # Provide the result to the user
        dispatcher.utter_message(text=f"Your estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")

        return []

    def calculate_carbon_footprint(self, responses):
        electricity_emissions = responses["electricity_kwh"] * EMISSION_FACTORS.get(responses["energy_source"], 0)
        car_emissions = responses["fuel_consumption"] * EMISSION_FACTORS.get(f"car_{responses['car_fuel_type']}", 0)
        flight_emissions = (responses["short_flights"] * 500 * EMISSION_FACTORS["air_travel"]) + \
                           (responses["long_flights"] * 2500 * EMISSION_FACTORS["air_travel"])
        diet_emissions = EMISSION_FACTORS.get(responses["diet"], 1.0)
        waste_emissions = 0.2 if responses["recycles"] == "no" else 0.16

        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions
        return total_emissions