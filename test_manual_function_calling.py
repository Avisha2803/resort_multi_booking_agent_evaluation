import google.generativeai as genai
from dotenv import load_dotenv
import os
from backend.tools import get_menu_items

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)

# Test without automatic function calling - manual handling
print("=" * 60)
print("Testing with MANUAL function calling...")
print("=" * 60)

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[get_menu_items],
    system_instruction="You are a restaurant agent. When asked for the menu, call get_menu_items and display the EXACT output."
)

chat = model.start_chat(enable_automatic_function_calling=False)

try:
    response = chat.send_message("Show me the menu")
    
    print(f"Response parts count: {len(response.parts)}")
    
    # Check if model wants to call a function
    for part in response.parts:
        if fn := part.function_call:
            print(f"Function call detected: {fn.name}")
            print(f"Arguments: {dict(fn.args)}")
            
            # Call the function manually
            if fn.name == "get_menu_items":
                menu_result = get_menu_items(**dict(fn.args))
                print(f"Function result length: {len(menu_result)}")
                
                # Send the function response back
                response2 = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name="get_menu_items",
                                response={"result": menu_result}
                            )
                        )]
                    )
                )
                print(f"Final response length: {len(response2.text)}")
                print(f"First 200 chars: {response2.text[:200]}")
        else:
            print(f"Text response: {part.text[:100] if hasattr(part, 'text') else 'No text'}")
            
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
