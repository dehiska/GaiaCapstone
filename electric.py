import requests

# Replace with your actual Climatiq API key
API_KEY = 'AS1VZA7S2747J2G2F8EGB3CKSZV7'  # Ensure this is the correct API key

# Define the endpoint and headers
url = "https://api.climatiq.io/estimate"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to get electricity estimate
def get_electricity_estimate(state_code, energy_amount):
    # Define the payload for the specified energy amount and state
    payload = {
        "emission_factor": {
            "activity_id": "electricity-supply_grid-source_supplier_mix",
            "data_version": "^0"
        },
        "parameters": {
            "energy": energy_amount,
            "energy_unit": "kWh"
        },
        "region": state_code 
    }

    try:
        # Make the request to the Climatiq API
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            co2e = data.get('co2e', 'N/A')
            co2e_unit = data.get('co2e_unit', 'N/A')
            calculation_method = data.get('co2e_calculation_method', 'N/A')
            emission_factor_name = data.get('emission_factor', {}).get('name', 'N/A')

            print(f"Electricity Estimate for {state_code} (for {energy_amount} kWh):")
            print(f"Estimated Emissions: {co2e} {co2e_unit}")
            print(f"Calculation Method: {calculation_method}")
            print(f"Emission Factor: {emission_factor_name}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())  # Print the response JSON to see the detailed error message
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Prompt the user for the state and amount of energy
state_code = input("Enter your state code (e.g., 'US-CA' for California): ")
energy_amount = float(input("Enter the amount of energy in kWh: "))

# Get the electricity estimate for the specified state and energy amount
get_electricity_estimate(state_code, energy_amount)