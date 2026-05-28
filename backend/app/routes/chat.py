from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter(prefix="/chat", tags=["Chat"])

from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

@router.post("")
async def chat_response(request: ChatRequest):
    query = request.message.lower()
    
    # 1. SPECIALIZED NUTRITION ENGINE
    import re
    weight_match = re.search(r'(\d+)\s*(kg|lbs)', query)
    height_match = re.search(r"(\d+)\s*(?:ft|')\s*(\d+)?", query)
    goal_match = re.search(r'(lose|reach|gain|bulk|cut)\s*(\d+)\s*(kg|lbs)', query)

    if weight_match and (height_match or goal_match):
        w = int(weight_match.group(1))
        target_w = int(goal_match.group(2)) if goal_match else w - 5
        
        if "lose" in query or (goal_match and target_w < w):
            return {"response": f"NEURAL ASSESSMENT: To drop from {w}kg to {target_w}kg, aim for 1,800-2,000 kcal/day. Prioritize high-volume low-calorie foods: Spinach, Egg Whites, and Lean Poultry. Limit 'Hidden Glycogen' (sauces/oils). Track your progress in the Elite HUD."}
        elif "gain" in query or "bulk" in query or (goal_match and target_w > w):
            return {"response": f"NEURAL ASSESSMENT: To scale from {w}kg to {target_w}kg, focus on a 300-500 kcal surplus (~2,800 kcal). Load up on Oats, Avocado, and Elite Whey. Heavy compound lifts are mandatory for this transformation."}

    # 2. ELITE KNOWLEDGE BASE
    responses = {
        "protein": "Elite standard: 1.8g per kg of bodyweight. Check the Store for our Hydrolyzed Whey.",
        "hiit": "Recovery is key. 48 hours between HIIT pulses is mandatory for neural recovery.",
        "fat": "Consistency > Intensity. Stay in a sustainable 300 kcal deficit and prioritize sleep.",
        "membership": "Visit our Membership hub. Elite Annual is our most optimized tier.",
        "diet": "Focus on whole foods. 80% clean, 20% flexibility. Avoid processed sugars to maintain peak hormonal balance."
    }
    
    for key in responses:
        if key in query:
            return {"response": responses[key]}
            
    return {"response": "That's an elite performance question. For a deep biological sync, ensure your profile data is complete in the HUD."}
