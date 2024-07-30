import requests
import json

# Function to get user input for origin and destination
def get_user_input():
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")
    return origin, destination

# API endpoint
url = "https://beta4.api.climatiq.io/estimate"

# Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Get user input for origin and destination
origin, destination = get_user_input()

# Data to be sent
data = {
    "emission_factor": {
        "activity_id": "electricity-supply_grid-source_residual_mix",
        "data_version": "^6"
    },
    "parameters": {
        "energy": 4200,
        "energy_unit": "kWh"
    }
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Check the response status and content
if response.status_code == 200:
    print("Success!")
    response_data = response.json()
    co2e = response_data.get('co2e')
    co2e_unit = response_data.get('co2e_unit')
    print(f"CO2e: {co2e} {co2e_unit}")
else:
    print(f"Failed with status code {response.status_code}")
    print("Response:", response.text)

# Print the origin and destination
print(f"Origin: {origin}")
print(f"Destination: {destination}")
