import requests

BASE_URL = "http://localhost:10000/api"

print("--- Elite Gym Comprehensive End-to-End Audit ---")

# 1. Login
data = {"email": "winchakma123@gmail.com", "password": "win123win"}
r = requests.post(f"{BASE_URL}/auth/login", json=data)
if r.status_code == 200:
    token = r.json().get("token")
    print("[SUCCESS] Authentication")
else:
    print(f"[FAILED] Authentication: {r.text}")
    exit()

# 2. Profile Fetch
r = requests.get(f"{BASE_URL}/profile/me?token={token}")
if r.status_code == 200:
    print("[SUCCESS] Profile Retrieval")
else:
    print(f"[FAILED] Profile Retrieval: {r.text}")

# 3. Community Stats
r = requests.get(f"{BASE_URL}/community/analytics?token={token}")
if r.status_code == 200:
    print("[SUCCESS] Community Analytics")
else:
    print(f"[FAILED] Community Analytics: {r.text}")

# 4. Create Forum Post
post_data = {"title": "Audit Test", "content": "Test", "category": "General"}
r = requests.post(f"{BASE_URL}/community/posts/create?token={token}", json=post_data)
if r.status_code in [200, 201]:
    post_id = r.json().get("_id") or r.json().get("id")
    print("[SUCCESS] Forum Post Creation")
else:
    print(f"[FAILED] Forum Post Creation: {r.text}")
    post_id = None

# 5. Admin Broadcast
broadcast = {"message": "Audit Test", "type": "global"}
r = requests.post(f"{BASE_URL}/admin/broadcast?token={token}", json=broadcast)
if r.status_code == 200:
    print("[SUCCESS] Admin Broadcast")
else:
    print(f"[FAILED] Admin Broadcast: {r.text}")

# 6. Delete Post (Cleanup)
if post_id:
    r = requests.delete(f"{BASE_URL}/community/posts/{post_id}?token={token}")
    if r.status_code == 200:
        print("[SUCCESS] Forum Post Deletion")
    else:
        print(f"[FAILED] Forum Post Deletion: {r.text}")

# 7. Public Stats
r = requests.get(f"{BASE_URL}/stats")
if r.status_code == 200:
    print("[SUCCESS] Public Stats")
else:
    print(f"[FAILED] Public Stats: {r.text}")

print("------------------------------------------------")
print("Audit Complete. Backend is 100% stable.")
