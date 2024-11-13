from unittest.mock import patch
import pytest
from lifestyleSurvey import LifestyleSurvey  # Adjust this import if needed

@pytest.fixture
def survey():
    return LifestyleSurvey()

@patch("builtins.input", side_effect=[
    "100",             # Response for initial electricity usage (in kWh)
    "natural gas",     # Energy source question
    "gasoline",        # Car fuel type question
    "75",              # Car miles driven question
    "mi",              # First response for distance unit question
    "kilometers",           
    "mi",              # Another valid unit as a backup
    "10",              # Car fuel consumption amount
    "gallons",         # Valid fuel unit
    "1",               # Number of short flights
    "1",               # Number of long flights
    "vegetarian",      # Diet question
    "yes"              # Recycling question
])
def test_ask_questions(mock_input, survey):
    """Test the ask_questions method by mocking user inputs."""
    survey.ask_questions()

    # Assertions to verify that the responses were stored correctly
    assert survey.responses["electricity_kwh"] == 400  # Electricity usage in kWh per week
    assert survey.responses["energy_source"] == "natural gas"
    assert survey.responses["car_fuel_type"] == "gasoline"
    assert survey.responses["car_miles"] == 300  # Miles driven per month
    assert survey.responses["gallons"] == 40  # Gallons of fuel consumed monthly
    assert survey.responses["short_flights"] == 1
    assert survey.responses["long_flights"] == 1
    assert survey.responses["diet"] == "vegetarian"
    assert survey.responses["recycles"] == "yes"

def test_display_results(survey, capsys):
    """Test the display_results method output."""
    survey.eco_score = 13.92  # Set known eco score based on your calculation
    survey.display_results()
    captured = capsys.readouterr()
    assert "Your estimated carbon footprint is 13.92 metric tons of CO2 per year." in captured.out


def test_display_results(survey, capsys):
    """Test the display_results method output with specific responses set."""
    survey.responses = {
        "electricity_kwh": 400,
        "energy_source": "natural gas",
        "car_fuel_type": "gasoline",
        "car_miles": 300,
        "gallons": 40,
        "short_flights": 1,
        "long_flights": 1,
        "diet": "vegetarian",
        "recycles": "yes"
    }
    
    # Call display_results which will calculate based on these values
    survey.display_results()
    
    # Capture the printed output and assert it matches the expected value
    captured = capsys.readouterr()
    assert "Your estimated carbon footprint is 23.23 metric tons of CO2 per year." in captured.out



    