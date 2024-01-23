import requests


def data_collection(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        # Process the response
        return response.json()
    else:
        print(f"Error: {response.status_code}")


def test_connection(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("Connection successful!")
        print(f"Status Code: {response.status_code}")
        print("Response Content:")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

