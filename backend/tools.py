from sqlalchemy.orm import Session
from .models import MenuItem, Order, ServiceRequest
from .database import SessionLocal
import json
from datetime import datetime
from pathlib import Path

# --- Database Helper ---
def get_db_session():
    return SessionLocal()

# --- Receptionist Tools ---
def check_room_availability(room_type: str = None):
    """
    Checks room availability.
    Args:
        room_type: Optional type of room (e.g., "Deluxe", "Suite").
    """
    # Mock logic with dynamic elements
    import random
    
    room_data = {
        "deluxe": {"base_price": 200, "count": 5},
        "suite": {"base_price": 500, "count": 2},
        "standard": {"base_price": 100, "count": 10}
    }
    
    req_type = room_type.lower() if room_type else "standard"
    # Mapping simple terms to keys
    if "suite" in req_type: key = "suite"
    elif "deluxe" in req_type: key = "deluxe"
    else: key = "standard"
    
    data = room_data[key]
    
    # Simulate availability randomly
    is_available = random.choice([True, True, False]) # Higher chance of availability
    
    if is_available:
        price = data["base_price"] + random.randint(-20, 50) # Dynamic pricing
        return f"Yes, we have {key.capitalize()} rooms available. The current rate is ${price} per night."
    else:
        return f"I'm sorry, but our {key.capitalize()} rooms are currently fully booked. Would you like to check another room type?"

def get_facility_info(facility_name: str):
    """
    Returns information about resort facilities.
    """
    facilities = {
        "gym": "The Gym is open from 6 AM to 10 PM. It is located on the 2nd floor.",
        "spa": "The Spa offers massages and treatments from 10 AM to 8 PM. Booking is required at extension 101.",
        "pool": "The Swimming Pool is open from 7 AM to 9 PM. Please wear appropriate swimwear.",
        "restaurant": "The Restaurant serves breakfast (7-10 AM), lunch (12-3 PM), and dinner (7-11 PM).",
        "checkin": "Check-in time is 2:00 PM.",
        "checkout": "Check-out time is 11:00 AM.",
        "wifi": "Free high-speed Wi-Fi is available throughout the resort. Network: 'ResortGuest', Password: 'relaxandenjoy'.",
        "parking": "Valet parking is complimentary for all guests."
    }
    
    # Simple fuzzy matching or direct lookup
    key = facility_name.lower()
    if "check" in key and "in" in key: return facilities["checkin"]
    if "check" in key and "out" in key: return facilities["checkout"]
    if "wifi" in key: return facilities["wifi"]
    if "park" in key: return facilities["parking"]
    
    return facilities.get(key, "I can answer questions about the Gym, Spa, Pool, Restaurant, Check-in/out times, Wi-Fi, and Parking.")

# --- Restaurant Tools ---

def get_menu_items(category: str = "all"):
    """
    Retrieves the menu from the text file.
    Args:
        category: Optional category filter.
    """
    try:
        # Get the project root directory (parent of backend/)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        menu_file = project_root / "menu_output.txt"
        
        with open(menu_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        return f"Error: Menu file not found at {menu_file}. Please ensure menu_output.txt exists in the project root."
    except Exception as e:
        return f"Error reading menu file: {str(e)}"

def place_restaurant_order(room_number: str, items_dict: dict):
    """
    Places a food order.
    Args:
        room_number: The guest's room number.
        items_dict: A dictionary of item names and quantities. e.g., {"Masala Dosa": 2, "Coffee": 1}
    """
    db = get_db_session()
    try:
        total_cost = 0
        valid_items = []
        
        # Validate items and calculate cost
        for item_name, quantity in items_dict.items():
            menu_item = db.query(MenuItem).filter(MenuItem.name.ilike(item_name)).first()
            if menu_item:
                total_cost += menu_item.price * quantity
                valid_items.append({"name": menu_item.name, "quantity": quantity, "price": menu_item.price})
            else:
                return f"Error: Item '{item_name}' is not on the menu."

        new_order = Order(
            room_number=room_number,
            items=valid_items,
            total_amount=total_cost,
            status="Pending"
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return f"Order placed successfully! Order ID: {new_order.id}. Total Bill: ₹{total_cost}."
    except Exception as e:
        return f"Failed to place order: {str(e)}"
    finally:
        db.close()

# --- Room Service Tools ---
def create_room_service_request(room_number: str, request_type: str, details: str = ""):
    """
    Creates a service request (cleaning, laundry, amenities).
    """
    db = get_db_session()
    try:
        new_request = ServiceRequest(
            room_number=room_number,
            request_type=request_type,
            details=details,
            status="Pending"
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return f"Service request created. Request ID: {new_request.id}. We will attend to it shortly."
    except Exception as e:
        return f"Failed to create request: {str(e)}"
    finally:
        db.close()
