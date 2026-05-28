import requests
import json

url = "http://localhost:10000/api/user/chat-brain?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3aW5jaGFrbWExMjNAZ21haWwuY29tIiwiZXhwIjoxNzgwMjU3Nzc4fQ.9WUGYT_IOQEMF_z5OOfbPLV0fqJsJxWpo6Rk75fyz00"
payload = {"message": "i want to lose weight"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
