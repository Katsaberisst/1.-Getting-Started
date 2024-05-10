#current weather Data

import requests

api_key = 'ea0df941c06d49b7bcb6ff698a93ab2a'

lat='-33.918861'
lon='18.423300'

url = 'https://api.openweathermap.org/data/2.5/weather'
complete_url = f"{url}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
response = requests.get(complete_url)

if response.status_code == 200:
    response_json = response.json()
    print (response_json)
else:
        print(f"error: {response.status_code}")
        raise requests.exceptions.HTTPError(response.text)


#Forecast

url = 'https://api.openweathermap.org/data/2.5/forecast'
complete_url = f"{url}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
response = requests.get(complete_url)

print("\nForecast\n")

if response.status_code == 200:
    response_json = response.json()
    print (response_json)
else:
        print(f"error: {response.status_code}")
        raise requests.exceptions.HTTPError(response.text)
