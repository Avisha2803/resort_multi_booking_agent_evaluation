from backend.tools import get_menu_items

try:
    print("Fetching menu...")
    menu = get_menu_items()
    
    # Write to file for better viewing
    with open("menu_output.txt", "w", encoding="utf-8") as f:
        f.write(menu)
    
    print("Menu has been written to menu_output.txt")
    print("\n" + "="*50)
    print(menu)
    print("="*50)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
