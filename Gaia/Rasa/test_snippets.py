from unittest.mock import patch, MagicMock
from snippets import estimate_emissions, endpoints


# Mock API response for successful emission estimation
mock_api_response_2 = {
    "data": {
        "attributes": {
            "emissions": 123.45
        }
    }
}

# Test for valid "Tobacco manufacturing" activity
@patch("builtins.input", side_effect=["Tobacco manufacturing", "100", "USD"])
@patch("requests.post")
def test_tobacco_manufacturing_activity(mock_post, mock_input):
    # Mock the requests.post call to return a predefined response
    mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_api_response_2)

    # Get the parameters for "Tobacco manufacturing" activity
    activity = "Tobacco manufacturing"
    activity_data = endpoints[activity]

    # Call the function
    result = estimate_emissions(api_key="mock-api-key")

    # Check if the API was called with the correct parameters
    mock_post.assert_called_once_with(
        "https://api.climatiq.io/estimate",
        headers={
            "Authorization": "Bearer mock-api-key",
            "Content-Type": "application/json"
        },
        json={
            "emission_factor": {
                "activity_id": activity_data["activity_id"],
                "data_version": "^0"
            },
            "parameters": {
                "money": 100.0,
                "money_unit": "USD"
            }
        }
    )

    # Ensure the result is as expected
    assert result == mock_api_response_2


# Test for invalid activity input with retry
@patch("builtins.input", side_effect=["Invalid Activity", "Tobacco manufacturing", "100", "USD"])
@patch("requests.post")
def test_retry_invalid_activity_choice(mock_post, mock_input):
    # Mock the requests.post call to return a predefined response
    mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_api_response_2)

    # Get the parameters for "Tobacco manufacturing" activity
    activity = "Tobacco manufacturing"
    activity_data = endpoints[activity]

    # Call the function
    result = estimate_emissions(api_key="mock-api-key")

    # Ensure the program first asks for an invalid activity and then retries with a valid one
    assert mock_input.call_count == 4  # Should ask for activity 4 times (1 invalid + 1 valid + 2 parameters)
    
    # Ensure the correct API parameters are used for the valid activity
    mock_post.assert_called_once_with(
        "https://api.climatiq.io/estimate",
        headers={
            "Authorization": "Bearer mock-api-key",
            "Content-Type": "application/json"
        },
        json={
            "emission_factor": {
                "activity_id": activity_data["activity_id"],
                "data_version": "^0"
            },
            "parameters": {
                "money": 100.0,
                "money_unit": "USD"
            }
        }
    )

    # Ensure the result is as expected
    assert result == mock_api_response_2

@patch("builtins.input", side_effect=["Tobacco manufacturing", "Invalid Amount", "Invalid Amount", "100", "USD"])
@patch("requests.post")
def test_retry_invalid_money_parameter(mock_post, mock_input):
    # Mock the requests.post call to return a predefined response
    mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_api_response_2)

    # Get the parameters for "Tobacco manufacturing" activity
    activity = "Tobacco manufacturing"
    activity_data = endpoints[activity]

    # Call the function
    result = estimate_emissions(api_key="mock-api-key")

    # Check the number of times input() was called
    assert mock_input.call_count == 5  # 3 calls for inputs + 2 retries for invalid money

    # Ensure the mock_post was called as expected (same as in your valid test)
    mock_post.assert_called_once_with(
        "https://api.climatiq.io/estimate",
        headers={
            "Authorization": "Bearer mock-api-key",
            "Content-Type": "application/json"
        },
        json={
            "emission_factor": {
                "activity_id": activity_data["activity_id"],
                "data_version": "^0"
            },
            "parameters": {
                "money": 100.0,
                "money_unit": "USD"
            }
        }
    )

    # Ensure the result is as expected
    assert result == mock_api_response_2