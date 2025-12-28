
from backend.agents import ResortAgent, restaurant_tools_list, RESTAURANT_PROMPT
import sys

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
    
    if "list index out of range" in response:
        print("\nSUCCESS: Reproduced the 'list index out of range' error.")
        sys.exit(0) # Exit 0 means we successfully reproduced the bug
    else:
        print("\nFAILURE: Did NOT reproduce the error. Response seems fine.")
        sys.exit(1)

except Exception as e:
    print(f"\nCRITICAL FAILURE: Script crashed with {e}")
    sys.exit(1)
