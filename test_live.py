import urllib.request
import json
from datetime import datetime

try:
    print("--- Testing against LIVE server ---")
    live_api = 'https://mygym-p9rd.onrender.com'
    
    # 1. Login
    login_data = json.dumps({'email': 'winchakma123@gmail.com', 'password': 'win123win'}).encode('utf-8')
    req = urllib.request.Request(f'{live_api}/api/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        login_resp = json.loads(response.read().decode())
        token = login_resp.get('token')
        print('Login Token:', token[:10] + '...')

    # 2. Fetch Workouts (Simulating the Heatmap fetch on Vercel)
    url = f'{live_api}/api/workouts/?token={token}'
    req2 = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    
    with urllib.request.urlopen(req2) as res2:
        workouts = json.loads(res2.read().decode())
        print(f'SUCCESS! Fetched {len(workouts)} workouts from the live server.')
        
        # Simulating the frontend counting logic
        workout_counts = [0] * 14
        today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        for w in workouts:
            w_date = datetime.fromisoformat(w['date'].replace('Z', '+00:00')) if isinstance(w.get('date'), str) else None
            if w_date:
                # Naive offset-naive subtraction for simplicity in test
                diff_time = abs((today_end - w_date.replace(tzinfo=None)).total_seconds())
                diff_days = int(diff_time // (24 * 3600))
                if 0 <= diff_days < 14:
                    workout_counts[13 - diff_days] += 1
                    
        print(f"\nLive Heatmap Workout Counts Array (13 days ago -> Today):")
        print(workout_counts)
        active_days = sum(1 for c in workout_counts if c > 0)
        print(f"Consistency: {round((active_days / 14) * 100)}%")

except Exception as e:
    print('Error:', e)
    if hasattr(e, 'read'):
        print(e.read().decode())
