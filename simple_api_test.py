import requests

print("Testing API endpoint...")
response = requests.post(
    'http://localhost:8000/chat',
    json={'history': [{'role': 'user', 'content': 'Show me the menu'}]}
)

result = response.json()
print(f"Status: {response.status_code}")
print(f"Response length: {len(result['response'])}")
print(f"Response preview: {result['response'][:200]}")
