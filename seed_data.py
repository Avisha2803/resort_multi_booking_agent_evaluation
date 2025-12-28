from backend.database import engine, SessionLocal, Base
from backend.models import MenuItem

# Create tables
Base.metadata.create_all(bind=engine)

def seed_menu():
    db = SessionLocal()
    
    # Check if menu already exists
    if db.query(MenuItem).count() > 0:
        print("Menu already seeded.")
        db.close()
        return

    menu_data = [
        {"name": "Masala Dosa", "description": "Crispy dosa with spiced potato filling", "price": 120, "category": "Breakfast"},
        {"name": "Plain Idli", "description": "Steamed rice cakes with chutney", "price": 80, "category": "Breakfast"},
        {"name": "Medu Vada", "description": "Fried lentil doughnuts", "price": 90, "category": "Breakfast"},
        {"name": "Upma", "description": "Semolina cooked with vegetables", "price": 100, "category": "Breakfast"},
        {"name": "Poha", "description": "Flattened rice with peanuts", "price": 100, "category": "Breakfast"},
        {"name": "Aloo Paratha", "description": "Stuffed paratha with curd", "price": 130, "category": "Breakfast"},
        {"name": "Paneer Paratha", "description": "Paneer stuffed paratha", "price": 150, "category": "Breakfast"},
        {"name": "Puri Bhaji", "description": "Fried bread with potato curry", "price": 140, "category": "Breakfast"},
        {"name": "Omelette", "description": "Indian-style omelette", "price": 90, "category": "Breakfast"},
        {"name": "Boiled Eggs", "description": "Two boiled eggs", "price": 70, "category": "Breakfast"},
    ]

    for item in menu_data:
        db_item = MenuItem(**item)
        db.add(db_item)
    
    db.commit()
    print("Menu seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_menu()
