import requests
import json

# Function to get user input for location and hotel nights
def get_user_input():
    location = input("Enter hotel city or country: ")
    hotel_nights = int(input("Enter number of hotel nights: "))
    return location, hotel_nights

# API endpoint
url = "https://beta4.api.climatiq.io/travel/hotel"

# Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Get user input for location and hotel nights
location, hotel_nights = get_user_input()

# Data to be sent
data = {
    "hotel_nights": hotel_nights,
    "location": {
        "query": location
    }
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Check the response status and content
if response.status_code == 200:
    response_data = response.json()
    # Extract co2e and co2e_unit if available
    co2e = response_data.get('co2e')
    co2e_unit = response_data.get('co2e_unit')
    if co2e is not None and co2e_unit is not None:
        print("Success!")
        print(f"CO2e: {co2e} {co2e_unit}")
    else:
        print("Success, but CO2e data not found in the response.")
else:
    print(f"Failed with status code {response.status_code}")
    print("Response:", response.text)

# Print the location and hotel nights
print(f"Location: {location}")
print(f"Hotel Nights: {hotel_nights}")
