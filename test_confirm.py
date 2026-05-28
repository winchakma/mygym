import re
msg = "i am 90 kg 163 cm want's to lose weight how much i have to burn and how much i have to eat?".lower()

weight_match = re.search(r'(\d+)\s*(kg|lbs|kilos|pounds)', msg)
height_match = re.search(r'(\d+)\s*(cm|inches|in)', msg)
goal_match = re.search(r'(lose|reach|gain|bulk|cut|weight|shred|maintenance)\s*(\d+)?', msg)

if (weight_match and goal_match) or ('macro' in msg) or ('how much' in msg and 'eat' in msg):
    if weight_match and goal_match:
        print('MACRO CALCULATION TRIGGERED SUCCESSFULLY')
    else:
        print('MACRO FALLBACK TRIGGERED')
else:
    print('FAILED TO RECOGNIZE MACRO INTENT')
