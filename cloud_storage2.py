from google.cloud import storage
import datetime
import os
import json
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
      #print('/n')
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

# Replace with the path to your downloaded JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "C:/Users/pc-Huawei/OneDrive/Έγγραφα/DataProjects/1. Getting Started/cloud-storage-admin-service-account.json"
print('environ')

  
def upload_json_to_gcs(json_data: dict, bucket_name: str, folder_path: str) -> None:
  """Uploads a JSON object to Google Cloud Storage.

  Args:
      json_data (dict): The JSON data to upload.
      bucket_name (str): The name of the bucket to upload the data to.
      folder_path (str): The folder path within the bucket to store the data (optional).
  """

  client = storage.Client()

  # Create a new bucket if it doesn't exist
  try:
    bucket = client.get_bucket(bucket_name)
  except:
    bucket = client.create_bucket(bucket_name)

  # Generate a timestamp for the filename
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

  # Define the file name with timestamp
  filename = f"{timestamp}.json"

  # Combine folder path and filename
  object_path = os.path.join(folder_path, filename)  # Using os.path.join for cleaner path handling

  # Convert JSON to bytes and upload
  blob = bucket.blob(object_path)
  blob.upload_from_string(json.dumps(json_data).encode("utf-8"), content_type="application/json")



  print("Uploading")
  #print(f"Uploaded {filename} to {bucket_name}/{object_path}")


bucket_name='weatherappdata'
folder_path='data1/'
#json_data='datatest.json'

print('call upload')
#print(f"Uploaded {weather_data} also {bucket_name} and {folder_path}")

try:
  #print(f"Uploaded {weather_data} also {bucket_name} and {folder_path}")
  print("call upload_json_to_gcs")
  upload_json_to_gcs(weather_data,bucket_name,folder_path)
  print("called upload_json_to_")
except Exception as error:
    # handle the exception
    print("An exception occurred:", error)
