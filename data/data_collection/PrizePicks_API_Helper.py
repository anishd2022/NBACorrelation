import requests


def data_collection(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        # Process the response
        return response.json()
    else:
        print(f"Error: {response.status_code}")
