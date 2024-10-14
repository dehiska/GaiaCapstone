from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os
from Gaia.Rasa.actions.snippets import endpoints, estimate_emissions

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Updated Emission Factors (in metric tons of CO2)
EMISSION_FACTORS = {
    "coal": 0.001,               # per kWh
    "petroleum": 0.00096,         # per kWh
    "natural_gas": 0.0004,        # per kWh
    "hydropower": 0.000019,       # per kWh
    "nuclear": 0.00000318,        # per kWh
    "car_gasoline": 0.0089,       # per gallon of gasoline
    "car_diesel": 0.01018,        # per gallon of diesel
    "intercity_rail": 0.00014,    # per passenger-mile
    "commuter_rail": 0.00017,     # per passenger-mile
    "bus": 0.00006,               # per passenger-mile
    "air_travel": 0.0002,         # per mile
    "meat_diet": 1.3,             # per year
    "average_omnivore": 1.0,      # per year
    "vegetarian": 0.66,           # per year
    "vegan": 0.56,                # per year
}

class ActionLifestyleSurvey(Action):
    def name(self) -> str:
        return "action_lifestyle_survey"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Get slot values from the conversation
        electricity_kwh = float(tracker.get_slot("electricity_kwh"))
        energy_source = tracker.get_slot("energy_source")
        car_fuel_type = tracker.get_slot("car_fuel_type")
        car_miles = float(tracker.get_slot("car_miles"))
        gallons = float(tracker.get_slot(f"{car_fuel_type}_gallons"))
        short_flights = int(tracker.get_slot("short_flights"))
        long_flights = int(tracker.get_slot("long_flights"))
        diet = tracker.get_slot("diet")
        recycles = tracker.get_slot("recycles")
        
        # Calculate emissions
        total_emissions = self.calculate_carbon_footprint(electricity_kwh, energy_source, car_fuel_type, car_miles, gallons, short_flights, long_flights, diet, recycles)
        
        # Dispatch the result back to the user
        dispatcher.utter_message(text=f"Your estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")
        return []

    def calculate_carbon_footprint(self, electricity_kwh, energy_source, car_fuel_type, car_miles, gallons, short_flights, long_flights, diet, recycles):
        # Energy source emissions
        electricity_emissions = electricity_kwh * 12 * EMISSION_FACTORS[energy_source]
        
        # Car fuel emissions
        car_emissions = gallons * EMISSION_FACTORS[f"car_{car_fuel_type}"]
        
        # Flight emissions
        flight_emissions = (short_flights * 500 * EMISSION_FACTORS["air_travel"]) + (long_flights * 2500 * EMISSION_FACTORS["air_travel"])
        
        # Diet emissions
        diet_emissions = EMISSION_FACTORS[diet]
        
        # Waste emissions (simplified for recycling impact)
        waste_emissions = 0.2 if recycles == "no" else 0.16
        
        # Total carbon footprint in metric tons
        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions
        return total_emissions






















"""
1) How much meat do you eat per week?
#First question is from: consumer_good-type_meat_and_offal NZ

2) Do you have solar energy?
3) How many people live in your home? 
4) Did you opt into clean energy from your utility company?
5) How many short haul flights did you fly last year? (1-3 hours)
6) How many medium haul flights did you fly last year? (3-6)
7) How many long haul flights did you fly last year? 6+
8) If you drive a car, what kind of car is it? Coupe, highlander, truck, etc.
9) How many miles do you drive per week? 
10) Do you have any other cars that you or the people you live with use? Repeat last 3 questions 

from actions import Action_Calculate_Emissions

class LifestyleSurveyAction:
    def __init__(self):
        self.questions = {1:"How much meat do you eat per week?", 2: ""}  # Dictionary to store parameter names as keys and questions as values
        self.responses = {}  # Dictionary to store parameter names as keys and user responses as values
        self.estimate_action = Action_Calculate_Emissions()
        self.eco_score = 0  # Attribute to store the total CO2 emissions score
    
    def create_survey(self, activity_id):
        # Get the required parameters from Action_estimate_emissions
        required_params = self.estimate_action.run(activity_id)
        
        # Create survey questions based on the parameters
        for param in required_params:
            question = f"What is the {param.replace('_', ' ')}?"
            self.questions[param] = question  # Store the question with the parameter name as the key
    
    def ask_questions(self):
        # Ask the questions and gather the user responses
        for param, question in self.questions.items():
            answer = input(question)
            self.responses[param] = answer  # Store the user's response in the responses dictionary
            self.estimate_action.set_parameter(param, answer)  # Pass the response to the Action_estimate_emissions class
    
    def calculate_emissions(self, activity_id):
        # Calculate emissions using Action_estimate_emissions
        emissions_result = self.estimate_action.estimate_emissions(activity_id, self.estimate_action.parameters)
        emission_value = emissions_result.get("emissions", 0)
        self.eco_score += float(emission_value)  # Add to eco-score for each question

    def complete_survey(self, activity_ids):
        # Loop through multiple activities, ask questions, and calculate emissions for each
        for activity_id in activity_ids:
            self.create_survey(activity_id)
            self.ask_questions()
            self.calculate_emissions(activity_id)
        
        # After 10 questions, display the total eco-score
        print(f"Your total CO2 emissions (eco-score) is: {self.eco_score} kg CO2e")

# Example usage in lifestyleSurvey.py:
if __name__ == "__main__":
    survey = LifestyleSurveyAction()
    
    # Assume 10 activities for example, in practice these would be replaced by real activity IDs
    activity_ids = ['travel', 'electricity', 'food_consumption', 'waste', 'transportation', 
                    'water_usage', 'clothing', 'appliances', 'heating', 'cooling']
    
    # Start the survey, ask questions, and calculate the eco-score
    survey.complete_survey(activity_ids)

"""