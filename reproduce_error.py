import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "history": [
        {"role": "user", "content": "Check room availability"}
    ]
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
