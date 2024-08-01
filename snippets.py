import requests
import os

# Define the different endpoints with their respective parameters
endpoints = {
    # Consumer Goods and Services
    "Tobacco manufacturing": {
        "activity_id": "consumer_goods-type_tobacco_products",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Breakfast cereals": {
        "activity_id": "consumer_goods-type_breakfast_cereals",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Breweries": {
        "activity_id": "consumer_goods-type_breweries_beer",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Amusement arcades": {
        "activity_id": "consumer_goods-type_amusement_parks_arcades",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Cable and subscription programming": {
        "activity_id": "consumer_goods-type_cable_subscription_programming",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Snack Foods": {
        "activity_id": "consumer_goods-type_snack_foods",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Dog and cat food": {
        "activity_id": "consumer_goods-type_dog_cat_food",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Dolls toys and games": {
        "activity_id": "consumer_goods-type_dolls_toys_games",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Flavored drink concentrates": {
        "activity_id": "consumer_goods-type_flavored_drink_concentrates",
        "parameters": {"money":"number", "money_unit":"text"}
    },

    # Health and Social Care
    "Residential mental health and substance abuse facilities": {
        "activity_id": "health_care-type_residential_mental_retardation_mental_health_substance_abuse_other_facilities",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Child day care": {
        "activity_id": "social_care-type_child_day_care",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Assisted living for the elderly": {
        "activity_id": "health_care-type_assisted_living_facilities_for_the_elderly",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Diagnostic imaging centers": {
        "activity_id": "health_care-type_diagnostic_imaging_centers",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Nursing and community care": {
        "activity_id": "health_care-type_nursing_community_care_facilities",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Blood sugar / pregnancy test kits": {
        "activity_id": "health_care-type_blood_sugar_pregnancy_other_diagnostic_test_kits",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "General Medical and Surgical Hospitals": {
        "activity_id": "health_care-type_general_medical_and_surgical_hospitals",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Healthcare practitioners (except physicians and dentists": {
        "activity_id": "health_care-type_healthcare_practitioners_except_physicians_dentists",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Outpatient healthcare": {
        "activity_id": "health_care-type_outpatient_healthcare",
        "parameters": {"money":"number", "money_unit":"text"}
    },

    # Organizational Activities
    "Civic and social organizations": {
        "activity_id": "organizational_activities-type_civic_social_professional_similar_organizations",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Grantmaking foundations": {
        "activity_id": "organizational_activities-type_grantmaking_giving_social_advocacy_organizations",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Religious organizations": {
        "activity_id": "organizational_activities-type_religious_organizations",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Computer systems design": {
        "activity_id": "professional_services-type_computer_systems_design",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Environmental consulting services": {
        "activity_id": "professional_services-type_environmental_other_technical_consulting_services",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Marketing consulting": {
        "activity_id": "professional_services-type_marketing_research_all_other_miscellaneous_professional_scientific_technical_services",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Travel agencies": {
        "activity_id": "professional_services-type_travel_arrangement_reservation",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Petroleum and petrol products": {
        "activity_id": "wholesale_trade-type_petroleum_petroleum_products",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Human rights organizations": {
        "activity_id": "organizational_activities-type_human_rights_organizations",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Political organizations": {
        "activity_id": "organizational_activities-type_political_organizations",
        "parameters": {"money":"number", "money_unit":"text"}
    },
    "Advertising agencies": {
        "activity_id": "professional_services-type_advertising_agencies",
        "parameters": {"money":"number", "money_unit":"text"}
    },

    # Transport  (distance unit may be km)
    "Bus": {
        "activity_id": "passenger_vehicle-vehicle_type_bus-fuel_source_na-distance_na-engine_size_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Motorcycle": {
        "activity_id": "passenger_vehicle-vehicle_type_motorcycle-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Light trucks": {
        "activity_id": "fuel-type_motor_gasoline-fuel_use_gasoline_light_duty_trucks",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Air transport": { #this may not work. may need to be more specific
        "activity_id": "transport-type_air_transport",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Commuter rail": {
        "activity_id": "passenger_train-route_type_commuter_rail-fuel_source_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Intercity rail (National average)": {
        "activity_id": "passenger_train-route_type_intercity-fuel_source_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Passenger car": {
        "activity_id": "passenger_vehicle-vehicle_type_car-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Transit rail (subway/tram)": {
        "activity_id": "passenger_train-route_type_transit_rail-fuel_source_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Military armored vehicles and tanks": {
        "activity_id": "military_vehicle-vehicle_type_armored_vehicles_tanks-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Guided missiles and space vehicles": {
        "activity_id": "military_vehicle-vehicle_type_guided_missiles_space_vehicles-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Motor homes": {
        "activity_id": "passenger_vehicle-vehicle_type_motor_homes-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Boats ": {
        "activity_id": "passenger_vehicle-vehicle_type_boat-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "Limousine and other chartering (bus, boat, car rental)": {
        "activity_id": "passenger_vehicle-vehicle_type_limousine_service-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
    "School bus": {
        "activity_id": "passenger_vehicle-vehicle_type_school_and_employee_bus_transportation-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        "parameters": {"distance": "number", "distance_unit": "text"}
    },
}

def get_endpoint_choice():
    print("Available activities:")
    for key in endpoints:
        print(key)

    choice = input("Enter the name of the activity you want to estimate emissions for: ")
    endpoint = endpoints.get(choice)

    if endpoint:
        return endpoint
    else:
        print("Invalid choice. Please try again.")
        return get_endpoint_choice()

def get_parameter_value(param_name, param_type):
    if param_type == "number":
        while True:
            try:
                value = float(input(f"Enter the value for {param_name.replace('_', ' ')}: "))
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:
        return input(f"Enter the value for {param_name.replace('_', ' ')}: ")
    

def estimate_emissions(api_key="AS1VZA7S2747J2G2F8EGB3CKSZV7"):

    if api_key is None:
        api_key = os.getenv('')
    
    if not api_key:
        raise ValueError("API key is required. Please set the CLIMATIQ_API_KEY environment variable or pass the API key as a parameter.")

    # Get user input for endpoint and its parameters
    endpoint = get_endpoint_choice()
    activity_id = endpoint["activity_id"]
    parameters = {}

    for param_name, param_type in endpoint["parameters"].items():
        parameters[param_name] = get_parameter_value(param_name, param_type)

    url = "https://api.climatiq.io/estimate"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "emission_factor": {
            "activity_id": activity_id,
            "data_version": "^0"
        },
        "parameters": parameters
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Example usage
if __name__ == "__main__":
    result = estimate_emissions()
    print(result)
