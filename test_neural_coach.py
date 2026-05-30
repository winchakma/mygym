import requests
import json
import uuid

API_BASE = "http://localhost:10000"

# 1. Register a fake user
fake_email = f"fakeuser_{uuid.uuid4().hex[:8]}@example.com"
register_data = {
    "firstName": "Fake",
    "lastName": "User",
    "email": fake_email,
    "phoneNumber": "1234567890",
    "password": "Password123!",
    "membershipType": "elite"
}

print("Registering user...")
headers = {"User-Agent": "Mozilla/5.0"}
r_reg = requests.post(f"{API_BASE}/api/auth/register", json=register_data, headers=headers)
print(f"Register status: {r_reg.status_code}")
if r_reg.status_code != 200:
    print(r_reg.text)
    exit(1)
token = r_reg.json().get("token")
print(f"Got token: {token[:10]}...")

# 2. Upload a workout proof (text)
print("\nUploading workout proof...")
workout_data = {
    "text_proof": "Did 100 pushups today"
}
r_work = requests.post(
    f"{API_BASE}/api/workouts/verify?token={token}",
    data=workout_data,
    headers={"Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}
)
print(f"Upload status: {r_work.status_code}")
print(r_work.json() if r_work.status_code == 200 else r_work.text)

# 3. Fetch workouts (simulate updateNeuralCoach)
print("\nFetching workouts...")
r_fetch = requests.get(
    f"{API_BASE}/api/workouts/?token={token}",
    headers={"Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}
)
print(f"Fetch status: {r_fetch.status_code}")
if r_fetch.status_code == 200:
    wData = r_fetch.json()
    print("wData is list?", isinstance(wData, list))
    if isinstance(wData, list):
        print(f"activeDays = {len(wData)}")
    else:
        print(f"wData keys: {wData.keys()}")
else:
    print(r_fetch.text)
