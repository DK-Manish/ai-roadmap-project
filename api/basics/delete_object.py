import requests

BASE_URL = "https://api.restful-api.dev"

# Replace with your actual ID
object_id = "7"

url = f"{BASE_URL}/objects/{object_id}"

response = requests.delete(url)

print("Status:", response.status_code)
print(response.json())