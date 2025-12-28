
from backend.agents import AgentManager
import sys

try:
    manager = AgentManager()
    print("AgentManager initialized.")
    
    # Test routing
    user_query = "I want to order a burger"
    route = manager.route_request(user_query)
    print(f"Query: '{user_query}' -> Route: {route}")
    
    if route == "Restaurant":
        print("Routing test PASSED")
    else:
        print("Routing test FAILED")
        sys.exit(1)

except Exception as e:
    print(f"Test FAILED with error: {e}")
    sys.exit(1)
