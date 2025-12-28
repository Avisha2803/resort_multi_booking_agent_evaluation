from backend.database import SessionLocal
from backend.models import MenuItem

def add_breakfast_items():
    db = SessionLocal()
    
    new_items = [
        # Breakfast Items
        {"name": "Idli Sambar", "description": "Steamed rice cakes with lentil soup", "price": 100, "category": "Breakfast"},
        {"name": "Masala Dosa", "description": "Crispy dosa with spiced potato filling", "price": 120, "category": "Breakfast"},
        {"name": "Poha", "description": "Flattened rice with peanuts and spices", "price": 80, "category": "Breakfast"},
        {"name": "Upma", "description": "Savory semolina porridge", "price": 90, "category": "Breakfast"},
        {"name": "Aloo Paratha", "description": "Stuffed flatbread with potato filling", "price": 110, "category": "Breakfast"},
        {"name": "Vada Sambar", "description": "Fried lentil donuts with lentil soup", "price": 100, "category": "Breakfast"},
        {"name": "Pancakes", "description": "Fluffy pancakes with maple syrup", "price": 150, "category": "Breakfast"},
        {"name": "French Toast", "description": "Bread dipped in egg and fried", "price": 130, "category": "Breakfast"},
        {"name": "Omelette", "description": "Three-egg omelette with vegetables", "price": 120, "category": "Breakfast"},
        {"name": "Boiled Eggs", "description": "Two boiled eggs", "price": 70, "category": "Breakfast"},
        {"name": "Bread Butter Jam", "description": "Toast with butter and jam", "price": 60, "category": "Breakfast"},
        {"name": "Cornflakes", "description": "Cornflakes with cold milk", "price": 90, "category": "Breakfast"},
        {"name": "Fresh Fruit Platter", "description": "Seasonal fresh fruits", "price": 140, "category": "Breakfast"},
    ]

    print("Adding breakfast menu items...")
    count = 0
    for item in new_items:
        # Check if item exists to avoid duplicates
        exists = db.query(MenuItem).filter(MenuItem.name == item["name"]).first()
        if not exists:
            db_item = MenuItem(**item)
            db.add(db_item)
            count += 1
            print(f"Added: {item['name']}")
        else:
            print(f"Skipped (already exists): {item['name']}")
            
    db.commit()
    db.close()
    print(f"\nSuccessfully added {count} breakfast items to the menu.")

if __name__ == "__main__":
    add_breakfast_items()
