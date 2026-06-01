import requests
import json

BASE_URL = "http://localhost:10000/api"

print("Starting Comprehensive Ecosystem Audit against Live Render Server...")
print("-" * 60)

# 1. Login
login_data = {
    "email": "winchakma123@gmail.com",
    "password": "win123win"
}
print("[1] Testing Authentication (Login)...")
try:
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if r.status_code == 200:
        token = r.json().get("access_token")
        print("    SUCCESS: Logged in as Admin.")
    else:
        print(f"    FAILED: {r.status_code} {r.text}")
        exit(1)
except Exception as e:
    print(f"    ERROR: {e}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. Profile Fetch
print("[2] Testing Profile Fetch...")
try:
    r = requests.get(f"{BASE_URL}/profile/me", headers=headers)
    if r.status_code == 200:
        print("    SUCCESS: Profile retrieved.")
    else:
        print(f"    FAILED: {r.status_code} {r.text}")
except Exception as e:
    print(f"    ERROR: {e}")

# 3. Community Stats
print("[3] Testing Community Analytics...")
try:
    r = requests.get(f"{BASE_URL}/community/analytics", headers=headers)
    if r.status_code == 200:
        print("    SUCCESS: Analytics retrieved.")
    else:
        print(f"    FAILED: {r.status_code} {r.text}")
except Exception as e:
    print(f"    ERROR: {e}")

# 4. Create Fake Post
print("[4] Testing Community Forums (Create Post)...")
post_data = {
    "title": "Audit Test Post",
    "content": "This is an automated test post to verify database synchronization.",
    "category": "Announcements"
}
post_id = None
try:
    r = requests.post(f"{BASE_URL}/community/posts/create", json=post_data, headers=headers)
    if r.status_code in [200, 201]:
        print("    SUCCESS: Test post created in database.")
        post_id = r.json().get("id") or r.json().get("_id")
    else:
        print(f"    FAILED: {r.status_code} {r.text}")
except Exception as e:
    print(f"    ERROR: {e}")

# 5. Admin Settings
print("[5] Testing Admin Privileges (Broadcast)...")
broadcast_data = {
    "message": "Audit Test Broadcast",
    "type": "global"
}
try:
    r = requests.post(f"{BASE_URL}/admin/broadcast", json=broadcast_data, headers=headers)
    if r.status_code == 200:
        print("    SUCCESS: Broadcast sent successfully.")
    else:
        # Might return 404 or 403 if endpoints don't match exactly, will check
        print(f"    FAILED/UNAVAILABLE: {r.status_code} {r.text}")
except Exception as e:
    print(f"    ERROR: {e}")

print("-" * 60)
print("Basic live API sanity check complete.")
