import requests
import json

# Function to get user input for origin and destination
def get_user_input():
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")
    cargo_weight = input('Enter the weight of the cargo')
    cargo_unit = input("Pounds or kilograms? (press p or k)")
    if cargo_unit == ('k'):
        lb_OR_kg = True
        return origin, destination, cargo_weight, lb_OR_kg
    elif cargo_unit == ('p'):
        lb_OR_kg = False
        return origin, destination, cargo_weight*0.45359237, lb_OR_kg

# API endpoint
url = "https://beta4.api.climatiq.io/freight/intermodal"

# Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Get user input for origin and destination
origin, destination, cargo_weight, lb_OR_kg = get_user_input()

# Data to be sent
data = {
    "route": [
        {
            "location": {
                "query": origin
            }
        },
        {
            "transport_mode": "road"
        },
        {
            "transport_mode": "air"
        },
        {
            "transport_mode": "road"
        },
        {
            "location": {
                "query": destination
            }
        }
    ],
    "cargo": {
        "weight": cargo_weight,
        "weight_unit": "kg"
    }
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Check the response status and content
if response.status_code == 200:
    response_data = response.json()
    # Extract co2e and co2e_unit
    co2e = response_data.get('co2e')
    co2e_unit = response_data.get('co2e_unit')
    print("Success!")

    if lb_OR_kg == True:
        print(f"CO2e: {co2e} {co2e_unit}")
    else:
        print(f"CO2e: {co2e*2.20462262}"+ "pounds")
else:
    print(f"Failed with status code {response.status_code}")
    print("Response:", response.text)

# Print the origin and destination
print(f"Origin: {origin}")
print(f"Destination: {destination}")
