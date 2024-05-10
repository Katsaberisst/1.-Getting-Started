import requests


def fetch_api_data(url: str) -> dict:


  response = requests.get(url)
  response.raise_for_status()  # Raise exception for non-200 status codes

  return response.json()

def get_weather_data(locations:dict, api_key: str) -> dict:
 
  base_url = "https://api.openweathermap.org/data/2.5/"
  weather_data = {"current": {}, "forecast": {}}

  for location_name, location in locations.items():
    try:
      # Construct URLs with common base and location data
      current_url = f"{base_url}weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}&units=metric"
      forecast_url = f"{base_url}forecast?lat={location['lat']}&lon={location['lon']}&appid={api_key}&units=metric"
      

      # Fetch and store data using a single function call
      weather_data["current"][location_name] = fetch_api_data(current_url)
      weather_data["forecast"][location_name] = fetch_api_data(forecast_url)
      #print (weather_data["current"][location_name])
      #print('\n')
      #print (weather_data["forecast"][location_name])

    except requests.exceptions.RequestException as e:
      print(f"Error fetching data for location {location_name}: {e}")

  return weather_data

api_key = '7d36a1fe418e725e09ae9090ebd0a64b' 

# Create a dictionary with the coordinates of 5 locations:
locations_dict = {
    'Thessaloniki, GR': {'lat': '40.6403', 'lon': '22.9439'},
    'Paris, FR': {'lat': '48.85341', 'lon': '2.3488'},
    'London, GB': {'lat': '51.50853', 'lon': '-0.12574'},
    'Dubai, AE': {'lat': '25.276987', 'lon': '55.296249'},
    'Los Angeles, US': {'lat': '34.0522', 'lon': '-118.2437'},
}

weather_data = get_weather_data(locations_dict, api_key)
print (weather_data['current'])