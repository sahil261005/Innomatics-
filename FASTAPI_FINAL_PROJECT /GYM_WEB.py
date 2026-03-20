from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI(title="IronFit Gym API")

# Fake Database
plans = [
    {"id": 1, "name": "Basic", "duration_months": 1, "price": 1000, "includes_classes": False, "includes_trainer": False},
    {"id": 2, "name": "Standard", "duration_months": 3, "price": 2800, "includes_classes": True, "includes_trainer": False},
    {"id": 3, "name": "Premium", "duration_months": 6, "price": 5000, "includes_classes": True, "includes_trainer": False},
    {"id": 4, "name": "Elite", "duration_months": 12, "price": 9000, "includes_classes": True, "includes_trainer": True},
    {"id": 5, "name": "Classes Only", "duration_months": 1, "price": 1500, "includes_classes": True, "includes_trainer": False},
]

memberships = []
membership_counter = 1

class_bookings = []
class_counter = 1

# Pydantic Models for Validation
class EnrollRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    plan_id: int = Field(..., gt=0)
    phone: str = Field(..., min_length=10)
    start_month: str = Field(..., min_length=3)
    payment_mode: str = "cash"
    referral_code: str = ""

class NewPlan(BaseModel):
    name: str = Field(..., min_length=2)
    duration_months: int = Field(..., gt=0)
    price: int = Field(..., gt=0)
    includes_classes: bool = False
    includes_trainer: bool = False

class ClassBookRequest(BaseModel):
    member_name: str
    class_name: str
    class_date: str

# Helper Functions
def find_plan(plan_id: int):
    for plan in plans:
        if plan["id"] == plan_id:
            return plan
    return None

def calculate_membership_fee(base_price: int, duration_months: int, payment_mode: str, referral_code: str):
    discount_percentage = 0
    if duration_months >= 12:
        discount_percentage = 20
    elif duration_months >= 6:
        discount_percentage = 10
    
    amount_after_duration_discount = base_price * (1 - discount_percentage / 100.0)
    
    referral_discount = 0.0
    if referral_code.strip() != "":
        referral_discount = amount_after_duration_discount * 0.05
        amount_after_duration_discount -= referral_discount
    
    processing_fee = 200 if payment_mode.lower() == "emi" else 0
    
    total_fee = amount_after_duration_discount + processing_fee
    
    return {
        "base": base_price,
        "duration_discount_pct": discount_percentage,
        "referral_discount_amount": referral_discount,
        "processing_fee": processing_fee,
        "total": total_fee
    }

def filter_plans_logic(max_price: Optional[int], max_duration: Optional[int], includes_classes: Optional[bool], includes_trainer: Optional[bool]):
    filtered = plans
    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]
    if max_duration is not None:
        filtered = [p for p in filtered if p["duration_months"] <= max_duration]
    if includes_classes is not None:
        filtered = [p for p in filtered if p["includes_classes"] == includes_classes]
    if includes_trainer is not None:
        filtered = [p for p in filtered if p["includes_trainer"] == includes_trainer]
    return filtered


# -------------------------
# ROUTES
# -------------------------

# Day 1: Home
@app.get("/")
def home():
    return {"message": "Welcome to IronFit Gym"}

# Day 1: Get all plans
@app.get("/plans")
def get_all_plans():
    prices = [p["price"] for p in plans]
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    return {
        "plans": plans,
        "total": len(plans),
        "min_price": min_price,
        "max_price": max_price
    }

# Day 1: Summary (Fixed Route)
@app.get("/plans/summary")
def get_plans_summary():
    if not plans:
        return {"total_plans": 0}
        
    classes_count = sum(1 for p in plans if p["includes_classes"])
    trainer_count = sum(1 for p in plans if p["includes_trainer"])
    
    cheapest = min(plans, key=lambda x: x["price"])
    expensive = max(plans, key=lambda x: x["price"])
    
    return {
        "total_plans": len(plans),
        "includes_classes_count": classes_count,
        "includes_trainer_count": trainer_count,
        "cheapest_plan": {"name": cheapest["name"], "price": cheapest["price"]},
        "most_expensive_plan": {"name": expensive["name"], "price": expensive["price"]}
    }

# Day 3: Filter Plans
@app.get("/plans/filter")
def filter_plans(
    max_price: Optional[int] = None,
    max_duration: Optional[int] = None,
    includes_classes: Optional[bool] = None,
    includes_trainer: Optional[bool] = None
):
    filtered = filter_plans_logic(max_price, max_duration, includes_classes, includes_trainer)
    return {"count": len(filtered), "plans": filtered}

# Day 6: Search
@app.get("/plans/search")
def search_plans(keyword: str):
    keyword = keyword.lower()
    matches = []
    
    for p in plans:
        # Check name
        if keyword in p["name"].lower():
            matches.append(p)
        # Check classes or trainer
        elif keyword == "classes" and p["includes_classes"] and p not in matches:
            matches.append(p)
        elif keyword == "trainer" and p["includes_trainer"] and p not in matches:
            matches.append(p)
            
    return {"total_found": len(matches), "plans": matches}

# Day 6: Sort
@app.get("/plans/sort")
def sort_plans(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "duration_months"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order field")
        
    sorted_p = sorted(plans, key=lambda x: x[sort_by] if isinstance(x[sort_by], int) else x[sort_by].lower(), reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "plans": sorted_p}

# Day 6: Page
@app.get("/plans/page")
def paginate_plans(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    sliced = plans[start:start+limit]
    total_pages = math.ceil(len(plans) / limit)
    
    return {
        "total": len(plans),
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "plans": sliced
    }

# Day 6: Browse (Combined Search, Sort, Page)
@app.get("/plans/browse")
def browse_plans(
    keyword: Optional[str] = None,
    includes_classes: Optional[bool] = None,
    includes_trainer: Optional[bool] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):
    if sort_by not in ["price", "name", "duration_months"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
        
    filtered = plans
    
    # Keyword search
    if keyword:
        keyword = keyword.lower()
        new_filtered = []
        for p in filtered:
            if keyword in p["name"].lower():
                new_filtered.append(p)
            elif keyword == "classes" and p["includes_classes"] and p not in new_filtered:
                new_filtered.append(p)
            elif keyword == "trainer" and p["includes_trainer"] and p not in new_filtered:
                new_filtered.append(p)
        filtered = new_filtered
        
    # Boolean filters
    if includes_classes is not None:
        filtered = [p for p in filtered if p["includes_classes"] == includes_classes]
    if includes_trainer is not None:
        filtered = [p for p in filtered if p["includes_trainer"] == includes_trainer]
        
    # Sort
    filtered = sorted(filtered, key=lambda x: x[sort_by] if isinstance(x[sort_by], int) else x[sort_by].lower(), reverse=(order == "desc"))
    
    # Paginate
    total_found = len(filtered)
    total_pages = math.ceil(total_found / limit) if total_found > 0 else 0
    start = (page - 1) * limit
    sliced = filtered[start:start+limit]
    
    return {
        "metadata": {
            "page": page,
            "limit": limit,
            "total_found": total_found,
            "total_pages": total_pages
        },
        "results": sliced
    }

# Day 4: Create Plan
@app.post("/plans", status_code=status.HTTP_201_CREATED)
def create_plan(new_plan: NewPlan):
    for p in plans:
        if p["name"].lower() == new_plan.name.lower():
            raise HTTPException(status_code=400, detail="Plan name already exists")
    
    new_id = max([p["id"] for p in plans] + [0]) + 1
    plan_dict = new_plan.model_dump()
    plan_dict["id"] = new_id
    plans.append(plan_dict)
    return {"message": "Plan created", "plan": plan_dict}

# Day 1: Get by ID (Variable Route)
@app.get("/plans/{plan_id}")
def get_plan_by_id(plan_id: int):
    plan = find_plan(plan_id)
    if not plan:
        return {"error": "Plan not found"}
    return plan

# Day 4: Update Plan
@app.put("/plans/{plan_id}")
def update_plan(
    plan_id: int, 
    price: Optional[int] = None, 
    includes_classes: Optional[bool] = None, 
    includes_trainer: Optional[bool] = None
):
    plan = find_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if price is not None:
        plan["price"] = price
    if includes_classes is not None:
        plan["includes_classes"] = includes_classes
    if includes_trainer is not None:
        plan["includes_trainer"] = includes_trainer
    return {"message": "Plan updated", "plan": plan}

# Day 4: Delete Plan
@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int):
    plan = find_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    for m in memberships:
        if m["plan_id"] == plan_id and m["status"] == "active":
            raise HTTPException(status_code=400, detail="Cannot delete plan with active memberships")
            
    plans.remove(plan)
    return {"message": f"Plan '{plan['name']}' deleted successfully"}


# Day 1: Get all memberships
@app.get("/memberships")
def get_all_memberships():
    return {"total": len(memberships), "memberships": memberships}

# Day 6: Memberships Search, Sort, Page
@app.get("/memberships/search")
def search_memberships(member_name: str):
    matches = [m for m in memberships if member_name.lower() in m["member_name"].lower()]
    return {"total": len(matches), "memberships": matches}

@app.get("/memberships/sort")
def sort_memberships(sort_by: str = "total_fee", order: str = "asc"):
    if sort_by not in ["total_fee", "duration_months"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
        
    sorted_m = sorted(memberships, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "memberships": sorted_m}

@app.get("/memberships/page")
def paginate_memberships(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    sliced = memberships[start:start+limit]
    return {"page": page, "limit": limit, "memberships": sliced}

# Day 2/3: Enroll POST
@app.post("/memberships", status_code=status.HTTP_201_CREATED)
def enroll_member(request: EnrollRequest):
    global membership_counter
    plan = find_plan(request.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    fee_details = calculate_membership_fee(
        plan["price"], 
        plan["duration_months"], 
        request.payment_mode, 
        request.referral_code
    )
    
    monthly_equivalent = fee_details["total"] / plan["duration_months"]
    
    record = {
        "membership_id": membership_counter,
        "member_name": request.member_name,
        "plan_id": plan["id"],
        "plan_name": plan["name"],
        "duration_months": plan["duration_months"],
        "monthly_equivalent_cost": round(monthly_equivalent, 2),
        "fee_breakdown": fee_details,
        "total_fee": fee_details["total"],
        "status": "active"
    }
    
    memberships.append(record)
    membership_counter += 1
    
    return {"message": "Membership created successfully", "membership": record}

# Day 5: Multi-Step - Freeze/Reactivate
@app.put("/memberships/{membership_id}/freeze")
def freeze_membership(membership_id: int):
    for m in memberships:
        if m["membership_id"] == membership_id:
            m["status"] = "frozen"
            return {"message": "Membership frozen successfully", "membership": m}
    raise HTTPException(status_code=404, detail="Membership not found")

@app.put("/memberships/{membership_id}/reactivate")
def reactivate_membership(membership_id: int):
    for m in memberships:
        if m["membership_id"] == membership_id:
            m["status"] = "active"
            return {"message": "Membership reactivated successfully", "membership": m}
    raise HTTPException(status_code=404, detail="Membership not found")


# Day 5: Class Bookings POST
@app.post("/classes/book")
def book_class(request: ClassBookRequest):
    global class_counter
    
    has_valid_membership = False
    for m in memberships:
        if m["member_name"].lower() == request.member_name.lower() and m["status"] == "active":
            plan = find_plan(m["plan_id"])
            if plan and plan["includes_classes"]:
                has_valid_membership = True
                break
                
    if not has_valid_membership:
        raise HTTPException(status_code=400, detail="Member does not have an active membership that includes classes.")
        
    booking = {
        "booking_id": class_counter,
        "member_name": request.member_name,
        "class_name": request.class_name,
        "class_date": request.class_date
    }
    
    class_bookings.append(booking)
    class_counter += 1
    
    return {"message": "Class booked successfully", "booking": booking}

# Day 5: Class Bookings GET
@app.get("/classes/bookings")
def get_class_bookings():
    return {"total": len(class_bookings), "bookings": class_bookings}

# Day 5: Class Bookings CANCEL
@app.delete("/classes/cancel/{booking_id}")
def cancel_class_booking(booking_id: int):
    for i, b in enumerate(class_bookings):
        if b["booking_id"] == booking_id:
            deleted = class_bookings.pop(i)
            return {"message": "Class booking cancelled successfully", "booking": deleted}
    raise HTTPException(status_code=404, detail="Booking not found")

