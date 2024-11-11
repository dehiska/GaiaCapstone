from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from snippets import endpoints, estimate_emissions
from rasa_sdk.events import FollowupAction
import requests

# Mappings for units
distance_unit_mapping = {
    "mi": "mi",
    "miles": "mi",
    "mile": "mi",
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
    
valid_recycles = ["yes", "no"]
valid_short_flights = [str(i) for i in range(0, 101)]
valid_long_flights = [str(i) for i in range(0, 101)]


class ActionLifestyleSurvey(Action):
    def name(self) -> str:
        return "action_lifestyle_survey"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        responses = {}

        # Step 1: Validate electricity usage
        electricity_kwh = tracker.get_slot("electricity_kwh")
        if electricity_kwh:
            try:
                # Attempt to convert the input directly to an integer
                electricity_kwh = int(electricity_kwh)
                responses["electricity_kwh"] = electricity_kwh
            except ValueError:
                try:
                    # If not an integer, attempt to convert to a float
                    electricity_kwh = float(electricity_kwh)
                    responses["electricity_kwh"] = electricity_kwh
                except ValueError:
                    # If conversion to both integer and float fails, prompt for a valid input
                    dispatcher.utter_message(text="Please provide a valid number for electricity usage in kWh.")
                    return []
        else:
            dispatcher.utter_message(text="Can you provide how many kWh of electricity you use per month?")
            return []

        # Step 2: Validate energy source
        energy_source = tracker.get_slot("energy_source")
        if not energy_source:
            dispatcher.utter_message(text="What is your main energy source (coal, petroleum, natural gas, hydropower, nuclear)?")
            return []
        responses["energy_source"] = energy_source


        
        # Step 3: Validate recycling
        recycles = tracker.get_slot("recycles")
        if recycles:
            try:
                # Check if input is valid (either "yes" or "no")
                if (str(recycles).strip().lower() in ["yes", "no"]):
                    responses["recycles"] = recycles.lower() == "yes"
                else:
                    raise ValueError("Invalid answer.")
            except ValueError:
                dispatcher.utter_message(text="Do you recycle (yes or no)?")
                return []
        else:
            dispatcher.utter_message(text="Do you recycle (yes or no)?")
            return []

        

        ## Step 4: Validate short flights
        short_flights = tracker.get_slot("short_flights")
        if short_flights:
            try:
                # Attempt to convert the input directly to an integer
                short_flights = int(short_flights)
                responses["short_flights"] = short_flights
            except ValueError:
                try:
                    # If not an integer, attempt to convert to a float
                    short_flights = float(short_flights)
                    responses["short_flights"] = int(short_flights)  # Convert to int for flight counts
                except ValueError:
                    # If conversion to both integer and float fails, prompt for a valid response
                    dispatcher.utter_message(text="Please provide a valid number of short flights.")
                    return []
        else:
            # Prompt the user if no input is provided
            dispatcher.utter_message(text="How many short flights (under 3 hours) do you take per year?")
            return []

        # Step 5: Validate long flights
        long_flights = tracker.get_slot("long_flights")
        if long_flights:
            try:
                # Attempt to convert the input directly to an integer
                long_flights = int(long_flights)
                responses["long_flights"] = long_flights
            except ValueError:
                try:
                    # If not an integer, attempt to convert to a float
                    long_flights = float(long_flights)
                    responses["long_flights"] = int(long_flights)  # Convert to int for flight counts
                except ValueError:
                    # If conversion to both integer and float fails, prompt for a valid response
                    dispatcher.utter_message(text="Please provide a valid number of long flights.")
                    return []
        else:
            # Prompt the user if no input is provided
            dispatcher.utter_message(text="How many long flights (over 3 hours) do you take per year?")
            return []

        # Step 6: Validate diet type
        diet = tracker.get_slot("diet")
        if not diet:
            dispatcher.utter_message(text="What is your diet type (meat diet, average omnivore, vegetarian, vegan)?")
            return []
        responses["diet"] = diet



        # Step 7: Validate car fuel type
        car_fuel_type = tracker.get_slot("car_fuel_type")
        if not car_fuel_type:
            dispatcher.utter_message(text="What fuel does your car use (gasoline (gas), or diesel)?")
            return []
        responses["car_fuel_type"] = car_fuel_type

        # Step 8: Validate car fuel unit
        car_fuel_unit = tracker.get_slot("car_fuel_unit")
        if car_fuel_unit not in ["gallons", "liters"]:
            dispatcher.utter_message(text="Do you measure your fuel in 'gallons' or 'liters'?")
            return []
        responses["car_fuel_unit"] = car_fuel_unit


        # Step 9: Validate driving distance
        car_miles = tracker.get_slot("car_miles")
        if car_miles:
            try:
                car_miles = float(car_miles)  # Allow single number inputs
                responses["car_miles"] = car_miles
            except ValueError:
                dispatcher.utter_message(text="Please provide a valid number of miles or kilometers.")
                return []
        else:
            dispatcher.utter_message(text="How many miles or kilometers do you drive per week?")
            return []

        # Step 10: Get the actual fuel consumption amount
        fuel_consumption = tracker.get_slot("car_fuel_usage")
        if fuel_consumption:
            try:
                fuel_consumption = float(fuel_consumption)
                responses["car_fuel_usage"] = fuel_consumption
            except ValueError:
                dispatcher.utter_message(text=f"Please provide a valid number for fuel consumption in {responses['car_fuel_unit']}.")
                return []
        else:
            dispatcher.utter_message(text=f"How many {responses['car_fuel_unit']} of fuel does your car consume weekly?")
            return []

        # End of the run method in ActionLifestyleSurvey
        dispatcher.utter_message(text="Thank you for completing the survey. Calculating your emissions...")
        total_emissions = self.calculate_carbon_footprint(responses)
        dispatcher.utter_message(text=f"Your estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")

        # Trigger survey completion action
        return [FollowupAction("action_lifestyle_survey_completion")]


    def calculate_carbon_footprint(self, responses):
        # Calculate emissions for each component
        electricity_emissions = responses["electricity_kwh"]  *  EMISSION_FACTORS.get(responses["energy_source"], 0)  #multiply by 12 because we want the answer to be annual not monthly
        car_emissions = responses["car_fuel_usage"] * EMISSION_FACTORS.get(f"car_{responses['car_fuel_type']}", 0)   #multiply by 54 because we want the answer to be annual not weekly
        flight_emissions = (responses["short_flights"] * 500 * EMISSION_FACTORS["air_travel"]) + \
                           (responses["long_flights"] * 2500 * EMISSION_FACTORS["air_travel"])
        diet_emissions = EMISSION_FACTORS.get(responses["diet"], 1.0)
        waste_emissions = 0.2 if not responses["recycles"] else 0.16

        
        # electricity_emissions = electricity_kwh * EMISSION_FACTORS.get(energy_source, 0)
        # car_emissions = gallons * EMISSION_FACTORS.get(f"car {car_fuel_type}", 0)
        # flight_emissions = (short_flights * 500 * EMISSION_FACTORS["air travel"]) + (long_flights * 2500 * EMISSION_FACTORS["air travel"])
        # diet_emissions = EMISSION_FACTORS.get(diet, 1.0)
        # waste_emissions = 0.2 if recycles == "no" else 0.16
    
        # # # Calculate emissions for each component
        # electricity_emissions = responses["electricity_kwh"] * EMISSION_FACTORS.get(responses["energy_source"], 0)
        # car_emissions = responses["car_fuel_usage"] * EMISSION_FACTORS.get(f"car_{responses['car_fuel_type']}", 0)
        # flight_emissions = (responses["short_flights"] * 500 * EMISSION_FACTORS["air_travel"]) + \
        #                    (responses["long_flights"] * 2500 * EMISSION_FACTORS["air_travel"])
        # diet_emissions = EMISSION_FACTORS.get(responses["diet"], 1.0)
        # waste_emissions = 0.2 if responses["recycles"] == "no" else 0.16
        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions *12
        return total_emissions
    
class ActionLifestyleSurveyCompletion(Action):
    def name(self) -> str:
        return "action_lifestyle_survey_completion"

    def run(self, dispatcher, tracker, domain):
        # Perform any final steps, such as storing data or confirming submission
        dispatcher.utter_message(text="The lifestyle survey is now complete.")
        
        # Trigger the frontend to redirect to recommendations
        return [FollowupAction("action_redirect_to_recommendations")]

class ActionRedirectToRecommendations(Action):
    def name(self) -> str:
        return "action_redirect_to_recommendations"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(json_message={"redirect": True})  # Send custom message to frontend
        return []