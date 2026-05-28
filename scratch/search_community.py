import os

filepath = r"c:\Users\user\Desktop\mygym\frontend\community.html"
keywords = ["agora", "agorartc", "incomingcalloverlay", "startdirectcall", "callOverlay", "ringtone"]

if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print("Searching for calling resources...")
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        matched = [k for k in keywords if k.lower() in line_lower]
        if matched:
            print(f"Line {idx+1} matches {matched}:")
            print(f"  {line.strip()[:120]}")
else:
    print("File not found")
