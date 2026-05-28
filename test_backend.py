import requests

API_BASE = "https://mygym-p9rd.onrender.com"

# test missing token
res = requests.get(f"{API_BASE}/api/workouts/")
print(f"No token: {res.status_code}") # Should be 422

# test with invalid token
res = requests.get(f"{API_BASE}/api/workouts/?token=invalid")
print(f"Invalid token: {res.status_code}") # Should be 401
