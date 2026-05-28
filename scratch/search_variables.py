import os

filepath = r"c:\Users\user\Desktop\mygym\frontend\community.html"
keywords = [
    "agoraClient", "localTracks", "remoteUsers", "currentCallPartner",
    "currentCallChannel", "currentCallType", "isMicMuted", "isVideoMuted",
    "audioCtx", "ringtoneInterval", "startDirectCall", "acceptCall",
    "declineCall", "hangUpCall", "joinAgoraChannel", "leaveAgoraChannel",
    "cleanUpCallState", "toggleCallMic", "toggleCallVideo", "playSyntheticTone",
    "startRingtone", "stopRingtone"
]

if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print("Scanning for residual references...")
    found_any = False
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        matched = [k for k in keywords if k.lower() in line_lower]
        if matched:
            found_any = True
            print(f"Line {idx+1} matches {matched}:")
            print(f"  {line.strip()[:140]}")
    if not found_any:
        print("No residual references found!")
else:
    print("File not found")
