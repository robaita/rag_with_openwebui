import requests
import json


query = 'give me the list of resume who have experience in AWS?'

headers = {"Content-Type": "application/json"}  # Important for JSON payload
payload = {"query": query}

api_url = "http://localhost:5000/api/query"  # Replace with your API URL
# api_url = "http://192.168.0.106:5000/api/query"

try:
    response = requests.post(
        api_url, headers=headers, data=json.dumps(payload)
    )
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error querying the API: {e}")
    