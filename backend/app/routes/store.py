from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.models.admin import Activity, Order
from app.routes.profile import get_current_user
from datetime import datetime

router = APIRouter(prefix="/store", tags=["Store"])

@router.post("/checkout")
async def store_checkout(data: dict, current_user: User = Depends(get_current_user)):
    # Create Order
    new_order = Order(
        userId=str(current_user.id),
        userEmail=current_user.email,
        userName=f"{current_user.firstName} {current_user.lastName}",
        items=data.get("items_summary", "Neural Gear Bundle"),
        total=float(data.get("total", 0)),
        paymentMethod=data.get("payment_method", "Unknown"),
        status="processing"
    )
    await new_order.insert()
    
    # Log Activity
    await Activity(
        userId=str(current_user.id),
        userEmail=current_user.email,
        action="Shop Purchase",
        details=f"Ordered: {new_order.items} - Total: ${new_order.total}"
    ).insert()
    
    # Reward Points
    points_earned = int(new_order.total // 10)
    current_user.points += points_earned
    await current_user.save()
    
    return {
        "status": "success", 
        "order_id": str(new_order.id), 
        "points_earned": points_earned,
        "user": current_user
    }
