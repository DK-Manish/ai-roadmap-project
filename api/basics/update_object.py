import requests

BASE_URL = "https://api.restful-api.dev"

# Replace with your actual ID
object_id = "7"

url = f"{BASE_URL}/objects/{object_id}"

payload = {
    "name": "Updated Laptop from Python",
    "data": {
        "year": 2026,
        "price": 1500
    }
}

response = requests.put(url, json=payload)

print("Status:", response.status_code)
print(response.json())