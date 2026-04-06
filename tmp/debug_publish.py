import requests

url = "http://127.0.0.1:8000/api/blogs/"
token = "030a580aa082fa0bf7b93b758008840d2ed971bd"

data = {
    "title": "Debug Blog from AI",
    "category": 1,
    "content": "Testing publishing from script to see backend errors.",
    "tags": ["java", "debug"],
    "status": "published"
}

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
