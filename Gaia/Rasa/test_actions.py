'''
import pytest
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from unittest.mock import patch
from rasa_sdk.events import SlotSet
import sys
from pathlib import Path

project_root = Path(r"C:\Users\J_dur\OneDrive\Desktop\GaiaCapstone\Gaia")
sys.path.append(str(project_root / "Rasa" / "actions"))

from actions.actions import ActionCalculateEmissions, ActionLifestyleSurvey
from actions.snippets import endpoints, estimate_emissions

@pytest.fixture
def dispatcher():
    return CollectingDispatcher()

@pytest.fixture
def tracker():
    return Tracker(
        sender_id="test_user",
        slots={
            "activity": "Passenger car",
            "distance": "1000",
            "distance_unit": "km",
        },
        latest_message={"intent": {"name": "calculate_emissions"}},
        events=[],
        latest_action_name="action_listen",
        paused=False,            # Default value for paused
        followup_action=None,    # Default value for followup_action
        active_loop=None         # Default value for active_loop
    )

@pytest.fixture
def action_calculate_emissions():
    # Creating a subclass for testing purposes
    class TestActionCalculateEmissions(ActionCalculateEmissions):
        def run(self, dispatcher, tracker, domain):
            activity_id = "passenger_vehicle-vehicle_type_car-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na"
            parameters = {"distance": 1000, "distance_unit": "mi"}

            # Mock the estimate_emissions function with the API key and parameters
            emissions_result = estimate_emissions(api_key="AS1VZA7S2747J2G2F8EGB3CKSZV7")
            # Sample response message
            message = f"The estimated emissions for Car are {emissions_result.get('total_emissions', 'unknown')} kg CO2."
            dispatcher.utter_message(text=message)

            # Return any slots or events as needed
            return [SlotSet("emission_estimate", emissions_result.get("total_emissions"))]

    return TestActionCalculateEmissions()

def test_action_calculate_emissions_all_slots_filled(dispatcher, tracker, action_calculate_emissions):
    # Run the action with all required slots filled
    with patch('actions.snippets.estimate_emissions', return_value={"total_emissions": 42}):
        events = action_calculate_emissions.run(dispatcher, tracker, {})

        # Validate that the dispatcher provided an output message
        messages = dispatcher.messages
        assert len(messages) > 0
        assert "The estimated emissions for Car are 42 kg CO2." in messages[0]["text"]

@pytest.fixture
def tracker():
    return Tracker(
        sender_id="test_user",
        slots={
            "activity": "car_gasoline",
            "distance_unit": "mi",
            "money_unit": "USD",
            "electricity_kwh": "100",
            "energy_source": "natural_gas",
            "car_fuel_type": "gasoline",
            "car_fuel_unit": "gallons",
            "car_fuel_usage": "10",
            "car_miles": "100",
            "short_flights": "2",
            "long_flights": "1",
            "diet": "vegetarian",
            "recycles": "yes",
        },
        latest_message={"intent": {"name": "ask_lifestyle_survey"}},
        events=[],
        latest_action_name="action_listen",
        paused=False,  # Default value
        followup_action=None,  # Default value
        active_loop=None  # Default value
    )


@pytest.fixture
def action_lifestyle_survey():
    return ActionLifestyleSurvey()

def test_action_calculate_emissions(dispatcher, tracker, action_calculate_emissions):
    # Run the action and capture events
    events = action_calculate_emissions.run(dispatcher, tracker, {})

    # Assert that the dispatcher provided an output message
    messages = dispatcher.messages
    assert len(messages) > 0
    assert "The estimated emissions for car_gasoline are" in messages[0]["text"]

    # Check for missing parameters edge case
    tracker.slots["activity"] = None
    events = action_calculate_emissions.run(dispatcher, tracker, {})
    assert "Could you specify an activity" in dispatcher.messages[-1]["text"]

    # Test invalid distance unit edge case
    tracker.slots["distance_unit"] = "invalid_unit"
    events = action_calculate_emissions.run(dispatcher, tracker, {})
    assert "Invalid distance unit" in dispatcher.messages[-1]["text"]

def test_action_lifestyle_survey(dispatcher, tracker, action_lifestyle_survey):
    # Run the action and capture events
    events = action_lifestyle_survey.run(dispatcher, tracker, {})

    # Validate a successful carbon footprint calculation
    messages = dispatcher.messages
    assert len(messages) > 0
    assert "Your estimated carbon footprint is" in messages[0]["text"]

    # Edge Case: Missing slots for survey questions
    tracker.slots["electricity_kwh"] = None
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "Could you provide how many kWh of electricity" in dispatcher.messages[-1]["text"]

    tracker.slots["energy_source"] = None
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "What is your main energy source" in dispatcher.messages[-1]["text"]

    tracker.slots["car_fuel_type"] = None
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "What fuel does your car use" in dispatcher.messages[-1]["text"]

    tracker.slots["car_fuel_unit"] = "invalid_unit"
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "Do you measure your fuel in 'gallons' or 'liters'" in dispatcher.messages[-1]["text"]

    # Test diet type edge case
    tracker.slots["diet"] = None
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "What is your diet type" in dispatcher.messages[-1]["text"]

    # Edge Case: Invalid recycling response
    tracker.slots["recycles"] = "maybe"
    action_lifestyle_survey.run(dispatcher, tracker, {})
    assert "Do you recycle" in dispatcher.messages[-1]["text"]
'''