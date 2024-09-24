import requests
import json

# Function to get user input for region, electricity amount, and unit
def get_user_input():
    region = input("Enter the region (e.g., US-CT): ")
    energy = float(input("Enter the energy amount: "))
    energy_unit = input("Enter the energy unit (e.g., kWh): ")
    return region, energy, energy_unit

# API endpoint
url = "https://beta4.api.climatiq.io/estimate"

# Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Get user input for region, energy amount, and energy unit
region, energy, energy_unit = get_user_input()

# Data to be sent
data = {
  "emission_factor": {
    "activity_id": "electricity-supply_grid-source_supplier_mix",
    "region": region,
    "data_version": "5.5"
  },
  "parameters": {
    "energy": energy,
    "energy_unit": energy_unit
  }
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Check the response status and content
if response.status_code == 200:
    response_data = response.json()
    print("Success!")
    print("Response:", json.dumps(response_data, indent=4))
else:
    print(f"Failed with status code {response.status_code}")
    print("Response:", response.text)
