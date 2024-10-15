from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os
from snippets import endpoints, estimate_emissions

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

EMISSION_FACTORS = {
    "coal": 0.001,
    "petroleum": 0.00096,
    "natural_gas": 0.0004,
    "hydropower": 0.000019,
    "nuclear": 0.00000318,
    "car_gasoline": 0.0089,
    "car_diesel": 0.01018,
    "air_travel": 0.0002,
    "meat_diet": 1.3,
    "average_omnivore": 1.0,
    "vegetarian": 0.66,
    "vegan": 0.56,
}

class LifestyleSurvey:
    def __init__(self):
        self.questions = {
            "electricity_kwh": "How many kWh of electricity do you use per month?",
            "energy_source": "What is your main energy source (coal, petroleum, natural_gas, hydropower, nuclear)?",
            "car_fuel_type": "What fuel does your car use (gasoline, diesel)?",
            "car_miles": "How many miles do you drive per month?",
            "gallons": "How many gallons of fuel does your car consume monthly?",
            "short_flights": "How many short flights (under 3 hours) do you take per year?",
            "long_flights": "How many long flights (over 3 hours) do you take per year?",
            "diet": "What is your diet type (meat_diet, average_omnivore, vegetarian, vegan)?",
            "recycles": "Do you recycle (yes or no)?"
        }
        self.responses = {}
        self.eco_score = 0

    def ask_questions(self):
        """Ask questions to the user and store responses."""
        for param, question in self.questions.items():
            self.responses[param] = input(f"{question} ")

    def calculate_carbon_footprint(self):
        """Calculate the total carbon footprint based on user responses."""
        electricity_kwh = float(self.responses.get("electricity_kwh", 0))
        energy_source = self.responses.get("energy_source", "natural_gas")
        car_fuel_type = self.responses.get("car_fuel_type", "gasoline")
        car_miles = float(self.responses.get("car_miles", 0))
        gallons = float(self.responses.get("gallons", 0))
        short_flights = int(self.responses.get("short_flights", 0))
        long_flights = int(self.responses.get("long_flights", 0))
        diet = self.responses.get("diet", "average_omnivore")
        recycles = self.responses.get("recycles", "yes")

        # Emissions calculations
        electricity_emissions = electricity_kwh * 12 * EMISSION_FACTORS.get(energy_source, 0)
        car_emissions = gallons * EMISSION_FACTORS.get(f"car_{car_fuel_type}", 0)
        flight_emissions = (short_flights * 500 * EMISSION_FACTORS["air_travel"]) + (long_flights * 2500 * EMISSION_FACTORS["air_travel"])
        diet_emissions = EMISSION_FACTORS.get(diet, 1.0)
        waste_emissions = 0.2 if recycles == "no" else 0.16

        # Total emissions
        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions
        self.eco_score = total_emissions
        return total_emissions

    def display_results(self):
        """Display the carbon footprint result to the user."""
        total_emissions = self.calculate_carbon_footprint()
        print(f"\nYour estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")


if __name__ == "__main__":
    survey = LifestyleSurvey()
    survey.ask_questions()
    survey.display_results()
