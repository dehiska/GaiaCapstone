import requests
import json





    # API endpoint
url = "https://api.climatiq.io/estimate"

    # Authorization token
headers = {
    "Authorization": "Bearer AS1VZA7S2747J2G2F8EGB3CKSZV7",  # Replace with your actual API key
    "Content-Type": "application/json"
}

def dumpjson(data):
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



print("Welcome to the Carbon Emissions Calculator")
print("\n")
print('US commercial and institutional building construction. 1')
print('US Emission intensity of supply chain (with margins i.e. cradle to shelf) in US dollars spend on: electrical contractors and other wiring installation contractors 2')
print('US Highway/bridge construction 3')
print('US Multifamily residential structures 4')
print('Nonresidential property manager 5')
print('Real estate brokers, agents, and estate appraisers 6')
print('colleges/universities 8')
print('Elementary and secondary schools 9')
print('Small electrical appliances 10')
print('Phones 11')
print('Air conditioning and warm air heating 12')
print('Computers 13')
print('External hard drives 14')
print('Data processing 15')
print('Aws, azure, GCP 16')
print('Portfolio management 17')
print('Securities and commodity exchanges 18')
print('Commercial banking 19')
print('Credit card issuing and credit unions 20')
print('trust/fund and financial vehicles 21')
print('International trade financing (US) 22')
print('Fertilizers containing NPK 23')
print('Cement 24')
print('Explosives manufacturing 25')
print('Plastics 26')
print('Drilling oil and gas wells 27')
print('Plastic bottles 28')
print('Hotel stay 29')
print('Full-service or limited-service restaurants 30')
print('Plastic waste for treatment: landfill 31')
print('Drinking water and wastewater treatment 32')
print('Sewage treatment facilities 33')
print('\n')


#
#FIRST CALCULATION
#
# Function to get user input for money value
def calculate_commercial_and_institutional_construction():
    money = float(input("Enter the money value: "))
    

    # Data to be sent
    data = {
        "emission_factor": {
            "activity_id": "construction-type_commercial_and_institutional_building_construction",
            "source": "EPA",
            "region": "US",
            "year": 2019,
            "source_lca_activity": "cradle_to_shelf",
            "data_version": "15.15"
        },
        "parameters": {
            "money": money,
            "money_unit": "usd"
        }
    }
    dumpjson(data)

def electrical_contractors_and_other_wiring_installation_contractors():
    print('Carpentors: Finish, flooring, or farming')
    type_of_contractor = int(input('Which type of contractor? e.g 1=finish, 2=flooring, 3=farming'))
    if type_of_contractor == 1:
        data = {
        "emission_factor": {
            "activity_id": "construction-type_electrical_contractors_and_other_wiring_installation_contractors",
            "source": "EPA",
            "region": "US",
            "year": 2019,
            "source_lca_activity": "cradle_to_shelf",
            "data_version": "15.15"
        },
        "parameters": {
            "money": float(input("Enter the money value: ")),
            "money_unit": "usd"
        }
    }
    elif type_of_contractor ==2:
        data = {
        "emission_factor": {
            "activity_id": "construction-type_flooring_contractors",
            "source": "EPA",
            "region": "US",
            "year": 2019,
            "source_lca_activity": "cradle_to_shelf",
            "data_version": "15.15"
        },
        "parameters": {
            "money": float(input("Enter the money value: ")),
            "money_unit": "usd"
        }
        }
    elif type_of_contractor == 3:
        data = {
        "emission_factor": {
            "activity_id": "construction-type_framing_contractors",
            "source": "EPA",
            "region": "US",
            "year": 2019,
            "source_lca_activity": "cradle_to_shelf",
            "data_version": "15.15"
        },
        "parameters": {
            "money": float(input("Enter the money value: ")),
            "money_unit": "usd"
        }
        }
    
    else:
        print("Invalid contractor type")
        return
    # Data to be sent
    
    dumpjson(data)


item_to_be_calculated = int(input('Please enter the number for what you want to calculate (e.g 1)'))
if item_to_be_calculated == 1:
    calculate_commercial_and_institutional_construction()
elif item_to_be_calculated == 2:
    electrical_contractors_and_other_wiring_installation_contractors()

elif item_to_be_calculated == 3:
    highway_bridge_construction()

















