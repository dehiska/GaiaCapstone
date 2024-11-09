from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
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
############################################## TESTING
class ActionCarousel(Action):

    def name(self) -> Text:
        return "actions_list"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        new_carousel = {
            "type": "template", 
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Air Jordan 1 Low",
                        "subtitle": "Price: $115",
                        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/53fa38ff-85be-4e83-82b0-2b3614667cb4/AIR+JORDAN+1+LOW.png",
                        "buttons": [
                            {
                                "title": "Details", 
                                "url": "https://www.nike.com/t/air-jordan-1-low-mens-shoes-0LXhbn/553558-042",
                                "type": "web_url"
                            },
                            {
                                "title": "Buy Now", 
                                "type": "postback",
                                "payload": "/buynow" # nly.yml
                            },
                            {
                                "title": "Size", 
                                "type": "postback",
                                "payload": "/size" # nly.yml
                            }
                        ]
                    },
                    {
                        "title": "Air Jordan 1 Retro High OG 'Midnight Navy'",
                        "subtitle": "Price: $180",
                        "image_url": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/9275d342-c34f-4d25-8641-17357e19d6f8/AIR+JORDAN+1+RETRO+HIGH+OG.png",
                        "buttons": [
                            {
                                "title": "Details", 
                                "url": "https://www.nike.com/t/air-jordan-1-retro-high-og-midnight-navy-mens-shoes-8xgDfd/DZ5485-401",
                                "type": "web_url"
                            },
                            {
                                "title": "Buy Now", 
                                "type": "postback",
                                "payload": "/buynow" # nly.yml
                            },
                            {
                                "title": "Size", 
                                "type": "postback",
                                "payload": "/size" # nly.yml
                            }
                        ]
                    }
                ] # ELEMENTS
            }
        }

        dispatcher.utter_message("Here are some of our Nike shoes!", attachment = new_carousel)

        return []
    
############################################ 2ND TEST
class ActionShowSurveyData(Action):

    def name(self) -> Text:
        return "action_show_survey_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        print("Slots:", tracker.slots) # debugging to verify data

        # Example: Retrieve survey data from slots
        survey_data = {
            "Diet": tracker.get_slot("diet_emissions") or "Not provided",
            "Recycles": tracker.get_slot("recycles_emissions") or "Not provided",
            "Electricity Emissions": tracker.get_slot("electricity_emissions") or "0",
            "Car Emissions": tracker.get_slot("car_emissions") or "0",
            "Flight Emissions": tracker.get_slot("flight_emissions") or "0",
            "Waste Emissions": tracker.get_slot("waste_emissions") or "0",
            "Total Emissions": tracker.get_slot("total_emissions") or "0",
        }

        diet = tracker.get_slot("diet") or "Not provided"
        recycles = tracker.get_slot("recycles") or "Not provided"

        response = f"Survey Data:\n- Diet: {diet}\n- Recycles:{recycles}"
        dispatcher.utter_message(response)

        return[]

        # Create carousel elements dynamically from survey data
        carousel_elements = []
        for key, value in survey_data.items():
            carousel_elements.append({
                "title": key,
                "subtitle": f"Value: {value}",
                "image_url": "https://via.placeholder.com/150",  # Placeholder image
                "buttons": [
                    {
                        "title": "Learn More",
                        "type": "postback",
                        "payload": f"/info_{key.lower().replace(' ', '_')}"
                    }
                ]
            })

        # Construct the carousel payload
        survey_carousel = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": carousel_elements
            }
        }

        # Send the carousel as a response
        dispatcher.utter_message(
            text="Here is your submitted survey data:",
            attachment=survey_carousel
        )

        print("Submitted Survey Data", survey_data)

        return [
            SlotSet(slot, value)
            for slot, value in survey_data.items()
        ]


############################################## TESTING
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
class ActionLifestyleSurvey(Action):
    def name(self) -> str:
        return "action_lifestyle_survey"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        responses = {}

        # Step 1: Check for electricity usage
        electricity_kwh = tracker.get_slot("electricity_kwh")
        if not electricity_kwh:
            dispatcher.utter_message(text="Could you provide how many kWh of electricity you use per month?")
            return []

        # Step 2: Check for main energy source
        energy_source = tracker.get_slot("energy_source")
        if not energy_source:
            dispatcher.utter_message(text="What is your main energy source (coal, petroleum, natural gas, hydropower, nuclear)?")
            return []

        # Step 3: Check for car fuel type
        car_fuel_type = tracker.get_slot("car_fuel_type")
        if not car_fuel_type:
            dispatcher.utter_message(text="What fuel does your car use (gasoline, gas, or diesel)?")
            return []

        # Step 4: Check for fuel unit (gallons or liters)
        car_fuel_unit = tracker.get_slot("car_fuel_unit")
        if car_fuel_unit not in ["gallons", "liters"]:
            dispatcher.utter_message(text="Do you measure your fuel in 'gallons' or 'liters'? Please specify either 'gallons' or 'liters'.")
            return []

        # Step 5: Get the actual fuel consumption amount
        fuel_consumption = tracker.get_slot("car_fuel_usage")
        if not fuel_consumption:
            dispatcher.utter_message(text=f"How many {car_fuel_unit} of fuel does your car consume weekly?")
            return []

        # Step 6: Check for driving distance
        car_miles = tracker.get_slot("car_miles")
        if not car_miles:
            dispatcher.utter_message(text="How many miles or kilometers do you drive per week?")
            return []

        # Step 7: Check for short flights
        short_flights = tracker.get_slot("short_flights")
        if not short_flights:
            dispatcher.utter_message(text="How many short flights (under 3 hours) do you take per year?")
            return []

        # Step 8: Check for long flights
        long_flights = tracker.get_slot("long_flights")
        if not long_flights:
            dispatcher.utter_message(text="How many long flights (over 3 hours) do you take per year?")
            return []

        # Step 9: Check for diet type
        diet = tracker.get_slot("diet")
        if not diet:
            dispatcher.utter_message(text="What is your diet type (meat diet, average omnivore, vegetarian, vegan)?")
            return []

        # Step 10: Check for recycling habit
        recycles = tracker.get_slot("recycles")
        if not recycles:
            dispatcher.utter_message(text="Do you recycle (yes or no)?")
            return []

        # Store validated slot values in responses dictionary
        responses = {
            "electricity_kwh": float(electricity_kwh) * 4,  # Convert weekly to monthly
            "energy_source": energy_source,
            "car_fuel_type": car_fuel_type,
            "car_fuel_unit": car_fuel_unit,
            "car_fuel_usage": float(fuel_consumption) * 4,  # Convert weekly to monthly
            "car_miles": float(car_miles) * 4,  # Convert weekly to monthly
            "short_flights": int(short_flights),
            "long_flights": int(long_flights),
            "diet": diet,
            "recycles": recycles
        }

        # Convert liters to gallons if necessary for consistent emissions calculation
        if car_fuel_unit == "liters":
            responses["car_fuel_usage"] *= 0.264172  # Liters to gallons conversion factor

        # Calculate emissions
        total_emissions = self.calculate_carbon_footprint(responses)
        dispatcher.utter_message(text=f"Your estimated carbon footprint is {total_emissions:.2f} metric tons of CO2 per year.")

        
        return []

    def calculate_carbon_footprint(self, responses):
        # Calculate emissions for each component
        electricity_emissions = responses["electricity_kwh"] * EMISSION_FACTORS.get(responses["energy_source"], 0)
        car_emissions = responses["car_fuel_usage"] * EMISSION_FACTORS.get(f"car_{responses['car_fuel_type']}", 0)
        flight_emissions = (responses["short_flights"] * 500 * EMISSION_FACTORS["air_travel"]) + \
                           (responses["long_flights"] * 2500 * EMISSION_FACTORS["air_travel"])
        diet_emissions = EMISSION_FACTORS.get(responses["diet"], 1.0)
        waste_emissions = 0.2 if responses["recycles"] == "no" else 0.16

        # Sum total emissions
        total_emissions = electricity_emissions + car_emissions + flight_emissions + diet_emissions + waste_emissions

        survey_data = {
        "electricity_emissions": electricity_emissions,
        "car_emissions": car_emissions,
        "flight_emissions": flight_emissions,
        "diet_emissions": diet_emissions,
        "waste_emissions": waste_emissions,
        "total_emissions": total_emissions
        }

        # Send the survey data to the Flask endpoint
        try:
            response = requests.post("http://localhost:5000/submit_survey", json=survey_data)
            if response.status_code == 200:
                print("Survey data submitted successfully.")
            else:
                print("There was an error submitting your survey data.")
        except requests.exceptions.RequestException as e:
            print("Failed to connect to the server. Error: {e}")

        return total_emissions


class ActionLifestyleSurveyCompletion(Action):
    def name(self) -> str:
        return "action_lifestyle_survey_completion"

    def run(self, dispatcher, tracker, domain):
        # Perform any final steps, such as storing data or confirming submission
        dispatcher.utter_message(text="The lifestyle survey is now complete.")
        
        # Trigger the frontend to redirect to recommendations
        return [FollowupAction("action_redirect_to_recommendations")]

# from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset

class ActionRedirectToRecommendations(Action):
    def name(self) -> str:
        return "action_redirect_to_recommendations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Send a custom JSON payload to trigger the redirect
        dispatcher.utter_message(
            json_message={
                "type": "redirect",
                "target_url": "/recommendations.html"
            }
        )
        return [AllSlotsReset()]
