"""AS1VZA7S2747J2G2F8EGB3CKSZV7"""
import requests
import json

url = "https://api.climatiq.io/data/v1/estimate"
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",
    "Content-Type": "application/json"
}

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

json_data = json.dumps(data)
response = requests.post(url, headers=headers, data=json_data)

if response.status_code == 200:
    print("Success!")
    print("Response:", response.json())
else:
    print(f"Failed with status code {response.status_code}")
    print("Response:", response.text)
