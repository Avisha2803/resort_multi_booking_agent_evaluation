import google.generativeai as genai
from dotenv import load_dotenv
import os
from backend.tools import get_menu_items

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)

# Test with automatic function calling
print("=" * 60)
print("Testing with automatic function calling...")
print("=" * 60)

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[get_menu_items],
    system_instruction="You are a restaurant agent. When asked for the menu, call get_menu_items and display the EXACT output."
)

chat = model.start_chat(enable_automatic_function_calling=True)

try:
    response = chat.send_message("Show me the menu")
    print(f"Response parts count: {len(response.parts) if hasattr(response, 'parts') else 'N/A'}")
    print(f"Response text length: {len(response.text) if hasattr(response, 'text') else 'N/A'}")
    if hasattr(response, 'text'):
        print(f"First 200 chars: {response.text[:200]}")
    
    if hasattr(response, 'prompt_feedback'):
        print(f"Prompt feedback: {response.prompt_feedback}")
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing direct function call...")
print("=" * 60)

# Test the function directly
result = get_menu_items()
print(f"Direct call result length: {len(result)}")
print(f"First 200 chars: {result[:200]}")
