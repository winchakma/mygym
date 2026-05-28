import re

msg = "i am 90 kg 163 cm want's to lose weight how much i have to burn and how much i have to eat?".lower()

weight_match = re.search(r'(\d+)\s*(kg|lbs)', msg)
height_match = re.search(r'(\d+)\s*(cm)', msg)
goal_match = re.search(r'(lose|reach|gain|bulk|cut|weight)\s*(\d+)?', msg)

print("Weight:", weight_match)
print("Height:", height_match)
print("Goal:", goal_match)

if weight_match and goal_match and ("how much" in msg or "burn" in msg or "eat" in msg):
    print("Macro Intent")
elif any(word in msg for word in ["calories in", "protein in", "carbs in", "nutrition for", "what is in"]):
    print("Food Intent")
else:
    print("General Intent")
