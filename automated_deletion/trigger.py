import requests

# Define the URL of the API
url = "https://sahanweerasiri.pythonanywhere.com/api/delete"

try:
    # Send the GET request
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        print("API call successful!")
        print("Response:", response.json())
    else:
        print(f"Failed to call the API. Status Code: {response.status_code}")
        print("Error:", response.text)
except Exception as e:
    print("An error occurred:", str(e))
