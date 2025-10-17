import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError 

# Load environment variables (GEMINI_API_KEY)
load_dotenv()

# Initialize the Gemini Client
try:
    # Uses the GEMINI_API_KEY from the .env file
    LLM_CLIENT = genai.Client()
    LLM_MODEL = "gemini-2.5-flash"
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    LLM_CLIENT = None

def generate_task_plan(goal_text: str) -> dict:
    """
    Calls the Gemini API to break down the goal into structured tasks (JSON).
    """
    if not LLM_CLIENT:
        return {"error": "LLM Client not initialized. Check GEMINI_API_KEY in .env."}

    if not goal_text:
        return {"error": "Goal text is required."}

    # CRUCIAL PROMPT: Instructs the AI to act as a PM and return strict JSON.
    system_prompt = (
        "You are an expert project manager and AI. Break down the user's goal into "
        "a list of actionable tasks. The output MUST be a VALID JSON object with "
        "a single key, 'tasks', which contains a list of task objects. "
        "Each task object must have the following keys: 'task' (string, the task name), "
        "'duration_days' (integer, estimated time), 'deadline_days' (integer, a cumulative deadline relative to today), "
        "and 'dependencies' (list of strings, naming prerequisite tasks). "
        "Be realistic and logical with dependencies and timelines."
    )
    
    try:
        response = LLM_CLIENT.models.generate_content(
            model=LLM_MODEL,
            contents=[
                {"role": "user", "parts": [{"text": system_prompt + "\n\nGoal: " + goal_text}]}
            ]
        )
        
        # Attempt to parse the text response as JSON
        json_string = response.text.strip()
        
        # Clean up common LLM output errors (e.g., surrounding markdown)
        if json_string.startswith('```json'):
            json_string = json_string[7:]
        if json_string.endswith('```'):
            json_string = json_string[:-3]
        
        return json.loads(json_string)

    except APIError as e:
        print(f"Gemini API Error: {e}")
        return {"error": f"LLM API Error: {e}"}

    except json.JSONDecodeError:
        return {"error": "AI service returned invalid or unparseable JSON. Try refining the prompt or goal."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == '__main__':
    # Test the function directly (requires a valid .env file)
    print("Testing LLM generation with a sample goal...")
    plan = generate_task_plan("Create a simple task manager app in Python in 10 days")
    print(json.dumps(plan, indent=2))