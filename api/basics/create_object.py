import requests

BASE_URL = "https://api.restful-api.dev"

url = f"{BASE_URL}/objects"

payload = {
    "name": "New Laptop",
    "data": {
        "year": 2025,
        "price": 1300
    }
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)

# can also use - print(response.json())