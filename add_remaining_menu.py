from backend.database import SessionLocal
from backend.models import MenuItem

def add_remaining_items():
    db = SessionLocal()
    
    new_items = [
        # Breads
        {"name": "Tandoori Roti", "description": "Whole wheat flatbread cooked in clay oven", "price": 40, "category": "Breads"},
        {"name": "Butter Naan", "description": "Soft leavened bread topped with butter", "price": 60, "category": "Breads"},
        {"name": "Garlic Naan", "description": "Naan infused with fresh garlic", "price": 70, "category": "Breads"},
        {"name": "Cheese Kulcha", "description": "Stuffed bread with cheese filling", "price": 90, "category": "Breads"},
        {"name": "Lachha Paratha", "description": "Layered whole wheat bread", "price": 65, "category": "Breads"},
        
        # Drinks
        {"name": "Mineral Water", "description": "1L bottled water", "price": 30, "category": "Drinks"},
        {"name": "Fresh Lime Soda", "description": "Refreshing lime drink (Sweet/Salted)", "price": 80, "category": "Drinks"},
        {"name": "Sweet Lassi", "description": "Traditional yogurt drink", "price": 90, "category": "Drinks"},
        {"name": "Masala Chai", "description": "Indian spiced tea", "price": 40, "category": "Drinks"},
        {"name": "Cold Coffee", "description": "Chilled coffee with vanilla ice cream", "price": 120, "category": "Drinks"},
        {"name": "Soft Drink", "description": "Coke/Sprite/Fanta (300ml)", "price": 50, "category": "Drinks"},
        
        # Miscellaneous
        {"name": "Green Salad", "description": "Sliced cucumber, tomato, carrot, onion", "price": 80, "category": "Miscellaneous"},
        {"name": "Masala Papad", "description": "Roasted papad topped with spicy salad", "price": 50, "category": "Miscellaneous"},
        {"name": "Boondi Raita", "description": "Yogurt with fried gram flour pearls", "price": 90, "category": "Miscellaneous"},
        {"name": "Plain Curd", "description": "Fresh plain yogurt", "price": 60, "category": "Miscellaneous"},
        {"name": "Pickle", "description": "Assorted Indian pickle", "price": 20, "category": "Miscellaneous"}
    ]

    print("Adding remaining menu items...")
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
    print(f"\nSuccessfully added {count} new items (Drinks, Breads, Misc).")

if __name__ == "__main__":
    add_remaining_items()
