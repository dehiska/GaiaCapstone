
import requests
import json

# Function to get user input for text and money
def get_user_input():
    text = input("Enter the text (e.g., material type): ")
    money = float(input("Enter the money value: "))
    return text, money

# API endpoint
url = "https://preview.api.climatiq.io/autopilot/v1-preview1/estimate"

# Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Get user input for text and money
text, money = get_user_input()

# Data to be sent
data = {
    "domain": "general",
    "text": text,
    "parameters": {
        "money": money,
        "money_unit": "usd"
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
