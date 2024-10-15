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
    "nauticl": "nmi",
    "nautical miles": "nmi"
}

fuel_unit_mapping = {
    "gallons": "gallons",
    "gallon": "gallons",
    "liters": "liters",
    "liter": "liters"
}

# Conversion factor for liters to gallons
LITERS_TO_GALLONS = 0.264172

# Conversion factor for kilometers to miles
KM_TO_MILES = 0.621371

# Emission factors without underscores
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


class LifestyleSurvey:
    def __init__(self):
        self.questions = {
            "electricity_kwh": "How many kWh of electricity do you use per week?",
            "energy_source": "What is your main energy source (coal, petroleum, natural gas, hydropower, nuclear)?",
            "car_fuel_type": "What fuel does your car use (gasoline, diesel, gas)?",
            "car_miles": "How many miles or kilometers do you drive per week?",
            "gallons": "How many gallons or liters of fuel does your car consume weekly?",
            "short_flights": "How many short flights (under 3 hours) do you take per year?",
            "long_flights": "How many long flights (over 3 hours) do you take per year?",
            "diet": "What is your diet type (meat diet, average omnivore, vegetarian, vegan)?",
            "recycles": "Do you recycle (yes or no)?"
        }
        self.responses = {}
        self.eco_score = 0

    def ask_question_with_validation(self, question, valid_responses=None, mapping=None):
        """Ask a question and validate the response."""
        while True:
            answer = input(question).lower()
            if valid_responses and answer not in valid_responses:
                print(f"Invalid answer. Please provide one of the following: {', '.join(valid_responses)}")
            elif mapping and answer not in mapping:
                print(f"Invalid unit. Please provide one of the following: {', '.join(mapping.keys())}")
            else:
                return answer

    def ask_numeric_question(self, question):
        """Ask a question expecting a numeric input and validate it."""
        while True:
            answer = input(question)
            try:
                return float(answer)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def ask_fuel_consumption(self):
        """Ask a question about fuel consumption, handling both value and unit."""
        while True:
            answer = input(self.questions["gallons"])
            parts = answer.lower().split()
            if len(parts) == 2:
                try:
                    value = float(parts[0])
                    unit = parts[1]
                    if unit in fuel_unit_mapping:
                        # Convert liters to gallons if necessary
                        if unit in ["liters", "liter"]:
                            value *= LITERS_TO_GALLONS
                        return value
                    else:
                        print(f"Invalid unit. Please use one of the following: {', '.join(fuel_unit_mapping.keys())}.")
                except ValueError:
                    print("Invalid input. Please provide a number followed by the unit (e.g., '10 gallons' or '10 liters').")
            else:
                # Ask for value and unit separately
                value = self.ask_numeric_question("Please enter the amount of fuel:")
                unit = self.ask_question_with_validation(
                    "Please enter the unit (gallons or liters):",
                    mapping=fuel_unit_mapping
                )
                # Convert liters to gallons if necessary
                if unit in ["liters", "liter"]:
                    value *= LITERS_TO_GALLONS
                return value

    def ask_questions(self):
        """Ask questions to the user and store responses."""
        # Weekly electricity use in kWh
        self.responses["electricity_kwh"] = self.ask_numeric_question(self.questions["electricity_kwh"]) * 4  # Convert to monthly

        # Energy source with error handling
        self.responses["energy_source"] = self.ask_question_with_validation(
            self.questions["energy_source"],
            valid_responses=EMISSION_FACTORS.keys()
        )

        # Car fuel type with "gas" added as an option
        self.responses["car_fuel_type"] = self.ask_question_with_validation(
            self.questions["car_fuel_type"],
            valid_responses=["gasoline", "diesel", "gas"]
        )

        # Car miles or kilometers with unit handling and numeric validation
        car_distance = self.ask_numeric_question(self.questions["car_miles"])
        distance_unit = self.ask_question_with_validation(
            "Is the distance in miles or kilometers?",
            mapping=distance_unit_mapping
        )
        if distance_unit == "km":
            car_distance *= KM_TO_MILES  # Convert kilometers to miles
        self.responses["car_miles"] = car_distance * 4  # Convert weekly to monthly

        # Fuel consumption with gallons or liters handling
        self.responses["gallons"] = self.ask_fuel_consumption() * 4  # Convert weekly to monthly

        # Flight information
        self.responses["short_flights"] = int(self.ask_numeric_question(self.questions["short_flights"]))
        self.responses["long_flights"] = int(self.ask_numeric_question(self.questions["long_flights"]))

        # Diet with error handling
        self.responses["diet"] = self.ask_question_with_validation(
            self.questions["diet"],
            valid_responses=EMISSION_FACTORS.keys()
        )

        # Recycling with error handling
        self.responses["recycles"] = self.ask_question_with_validation(
            self.questions["recycles"],
            valid_responses=["yes", "no"]
        )

    def calculate_carbon_footprint(self):
        """Calculate the total carbon footprint based on user responses."""
        electricity_kwh = self.responses.get("electricity_kwh", 0)
        energy_source = self.responses.get("energy_source", "natural gas")
        car_fuel_type = self.responses.get("car_fuel_type", "gasoline")
        car_miles = self.responses.get("car_miles", 0)
        gallons = self.responses.get("gallons", 0)
        short_flights = self.responses.get("short_flights", 0)
        long_flights = self.responses.get("long_flights", 0)
        diet = self.responses.get("diet", "average omnivore")
        recycles = self.responses.get("recycles", "yes")

        # Emissions calculations
        electricity_emissions = electricity_kwh * EMISSION_FACTORS.get(energy_source, 0)
        car_emissions = gallons * EMISSION_FACTORS.get(f"car {car_fuel_type}", 0)
        flight_emissions = (short_flights * 500 * EMISSION_FACTORS["air travel"]) + (long_flights * 2500 * EMISSION_FACTORS["air travel"])
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
