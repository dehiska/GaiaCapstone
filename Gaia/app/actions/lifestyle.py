from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet, UserUtteranceReverted, EventType
from rasa_sdk.types import DomainDict
import requests
import os
from Gaia.Rasa.actions.snippets import endpoints, estimate_emissions


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
"""

class surveyAction(Action):
    def __init__(self):
        self.api_key = os.getenv('CLIMATIQ_API_KEY')

    def ask_question(self, question: str) -> str:
        answer = input(question)
        return answer

    def calculate_emission(self, activity_id: str, parameters: dict) -> dict:
        url = "https://api.climatiq.io/estimate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }