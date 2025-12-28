from backend.database import SessionLocal
from backend.models import MenuItem

def add_menu_items():
    db = SessionLocal()
    
    new_items = [
        # Veg Starters
        {"name": "Paneer Tikka", "description": "Grilled cottage cheese with spices", "price": 240, "category": "Veg Starter"},
        {"name": "Veg Manchurian", "description": "Vegetable balls in spicy sauce", "price": 200, "category": "Veg Starter"},
        {"name": "Crispy Corn", "description": "Fried corn kernels with pepper", "price": 180, "category": "Veg Starter"},
        
        # Non-Veg Starters
        {"name": "Chicken Tikka", "description": "Tandoori grilled chicken chunks", "price": 320, "category": "Non-Veg Starter"},
        {"name": "Chilli Chicken", "description": "Spicy fried chicken with bell peppers", "price": 300, "category": "Non-Veg Starter"},
        {"name": "Fish Fry", "description": "Crispy fried fish fillet", "price": 350, "category": "Non-Veg Starter"},
        
        # Veg Main Course
        {"name": "Paneer Butter Masala", "description": "Cottage cheese in rich tomato gravy", "price": 300, "category": "Veg Main Course"},
        {"name": "Dal Makhani", "description": "Creamy black lentils slow cooked", "price": 250, "category": "Veg Main Course"},
        {"name": "Veg Biryani", "description": "Aromatic rice with mixed vegetables", "price": 280, "category": "Veg Main Course"},
        
        # Non-Veg Main Course
        {"name": "Butter Chicken", "description": "Chicken in creamy tomato sauce", "price": 380, "category": "Non-Veg Main Course"},
        {"name": "Mutton Rogan Josh", "description": "Kashmiri style mutton curry", "price": 450, "category": "Non-Veg Main Course"},
        {"name": "Chicken Biryani", "description": "Fragrant rice layered with spiced chicken", "price": 350, "category": "Non-Veg Main Course"},
        
        # Desserts
        {"name": "Gulab Jamun", "description": "Fried milk dumplings in sugar syrup", "price": 120, "category": "Desserts"},
        {"name": "Rasmalai", "description": "Soft paneer patties in sweetened milk", "price": 150, "category": "Desserts"},
        {"name": "Vanilla Ice Cream", "description": "Classic vanilla scoop", "price": 100, "category": "Desserts"},
        {"name": "Chocolate Brownie", "description": "Warm brownie with chocolate sauce", "price": 180, "category": "Desserts"}
    ]

    print("Adding new menu items...")
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
    print(f"\nSuccessfully added {count} new items to the menu.")

if __name__ == "__main__":
    add_menu_items()
