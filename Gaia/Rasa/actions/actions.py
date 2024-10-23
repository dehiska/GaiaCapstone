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


class ActionLifestyleSurvey(Action):
    def name(self) -> str:
        return "action_lifestyle_survey"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        electricity_kwh = (tracker.get_slot("electricity_kwh"))
        


        if electricity_kwh is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify how much electricity?")
            return []

        energy_source = tracker.get_slot("energy_source")
        if energy_source is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify an energy source?")
            return []

        car_fuel_type = tracker.get_slot("car_fuel_type")
        if car_fuel_type is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your car fuel type?")
            return []

        car_miles = (tracker.get_slot("car_miles"))
        if car_miles is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your car car miles?")
            return []

        gallons = tracker.get_slot("fuel_consumption")  # Correct slot name
        if gallons is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your gallons?")
        return []


        short_flights = (tracker.get_slot("short_flights"))
        if short_flights is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your short flights?")
            return []

        long_flights = (tracker.get_slot("long_flights"))
        if long_flights is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your long flights?")
            return []

        diet = tracker.get_slot("diet")
        if diet is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your diet?")
            return []

        recycles = tracker.get_slot("recycles")
        if recycles is None:
            dispatcher.utter_message(text="I didn't catch that. Could you specify your recycles?")
            return []

        total_emissions = self.calculate_carbon_footprint(electricity_kwh, energy_source, car_fuel_type, car_miles,
                                                          gallons, short_flights, long_flights, diet, recycles)

        dispatcher.utter_message(
            text=f"Your estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")
        return []

    def calculate_carbon_footprint(self, electricity_kwh, energy_source, car_fuel_type, car_miles, gallons,
                                   short_flights, long_flights, diet, recycles):
        electricity_emissions = electricity_kwh * 12 * EMISSION_FACTORS[energy_source]
        car_emissions = gallons * EMISSION_FACTORS[f"car_{car_fuel_type}"]
        flight_emissions = (short_flights * 500 * EMISSION_FACTORS["air_travel"]) + (
                    long_flights * 2500 * EMISSION_FACTORS["air_travel"])
        diet_emissions = EMISSION_FACTORS[diet]
        waste_emissions = 0.2 if recycles == "no" else 0.16

        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions
        return total_emissions


class ActionOpenAICall(Action):
    def name(self) -> str:
        return "action_openai_call"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get('text')

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_message,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )

            openai_response = response.choices[0].text.strip()
            dispatcher.utter_message(text=openai_response)

        except Exception as e:
            dispatcher.utter_message(text=f"Error: {str(e)}")

        return []


# Helper Class: LifestyleSurveyAction
class LifestyleSurveyAction:
    def __init__(self):
        self.questions = {1: "How much meat do you eat per week?", 2: ""}  # Dictionary to store questions
        self.responses = {}
        self.estimate_action = ActionCalculateEmissions()
        self.eco_score = 0

    def create_survey(self, activity_id):
        required_params = self.estimate_action.run(activity_id)
        for param in required_params:
            question = f"What is the {param.replace('_', ' ')}?"
            self.questions[param] = question

    def ask_questions(self):
        for param, question in self.questions.items():
            answer = input(question)
            self.responses[param] = answer
            self.estimate_action.set_parameter(param, answer)

    def calculate_emissions(self, activity_id):
        emissions_result = self.estimate_action.estimate_emissions(activity_id, self.estimate_action.parameters)
        emission_value = emissions_result.get("emissions", 0)
        self.eco_score += float(emission_value)

    def complete_survey(self, activity_ids):
        for activity_id in activity_ids:
            self.create_survey(activity_id)
            self.ask_questions()
            self.calculate_emissions(activity_id)

        print(f"Your total CO2 emissions (eco-score) is: {self.eco_score} kg CO2e")
