import traceback
from backend.agents import ResortAgent, restaurant_tools_list, RESTAURANT_PROMPT

try:
    print("Initializing ResortAgent (Restaurant)...")
    agent = ResortAgent(RESTAURANT_PROMPT, restaurant_tools_list)
    
    # Simulate the chat history structure
    history = [
        {"role": "user", "content": "Show me the menu"}
    ]
    
    print("Processing message 'Show me the menu'...")
    response = agent.process_message(history)
    print("Response received:")
    print(response)
    print(f"\nResponse length: {len(response)}")
    
except Exception as e:
    print(f"\nException occurred: {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
