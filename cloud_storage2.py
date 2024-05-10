from google.cloud import storage
import datetime
import os
import json

# Replace with the path to your downloaded JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "C:/Users/pc-Huawei/OneDrive/Έγγραφα/DataProjects/cloud-storage-admin-service-account.json"

bucket_name='weatherappdata'
folder_path='data1/'
json_data='datatest.json'
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
  except:       bucket = client.create_bucket(bucket_name)

  # Generate a timestamp for the filename
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

  # Define the file name with timestamp
  filename = f"{timestamp}.json"

  # Combine folder path and filename
  object_path = os.path.join(folder_path, filename)  # Using os.path.join for cleaner path handling

  # Convert JSON to bytes and upload
  blob = bucket.blob(object_path)
  blob.upload_from_string(json.dumps(json_data).encode("utf-8"), content_type="application/json")

  print(f"Uploaded {filename} to {bucket_name}/{object_path}")