import requests

BASE_URL = "https://api.restful-api.dev"

url = f"{BASE_URL}/objects/7"

response = requests.get(url)

print("Status:", response.status_code)

data = response.json()

print("Name:", data["name"])
print("Price:", data["data"]["price"])

# also can be - print(data)