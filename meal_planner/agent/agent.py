from typing import Optional
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.runners import InMemoryRunner
import asyncio
from dotenv import load_dotenv
from google.genai.types import Content, Part
import json
import pickle

load_dotenv()



# Step 1: Create the agent.
mindy_agent = LlmAgent(
    name="nutritionist",
    model="gemini-2.5-flash",
    instruction=(
        """
        You are Mindy, a compassionate nutritionist specializing in the MIND diet. 
        Your mission is to help users achieve their health goals by recommending 
        meal plans and complete recipes that follow MIND diet principles. 
        You actively listen to users, ask about their milestones, feelings, 
        and personal goals, and use this information to provide personalized, 
        motivating, and supportive guidance. Always encourage users, celebrate their 
        progress, and adapt your recommendations to their unique needs 
        and preferences.
        """
    ), 
    tools = [PreloadMemoryTool()],
)

# Create the runner for the agent
runner = InMemoryRunner(agent=mindy_agent)

async def _ask_mindy_for_meal_plan(
    selected_foods,
    user_id,
    session_id,
):
    """This function requests a meal plan from the Mindy Agent.
    Inputs: selected_foods
    Output: Meal Plan in Json Format."""

    # Build the prompt
    foods_str = ", ".join(selected_foods)
    prompt = (
        f"Based on the following selected foods: {foods_str}, "
        "please create a weekly meal plan following the mind diet."
        "Include complete recipes for each meal."
        "Return the result as a JSON object only using the below forma. Don't include anything outside this json structure. Format:\n"
        "{\n"
        '  "week": [\n'
        '    {\n'
        '      "day": "Monday",\n'
        '      "meals": [\n'
        '        {\n'
        '          "name": "Breakfast",\n'
        '          "recipe": {\n'
        '            "title": "Oatmeal with Berries",\n'
        '            "ingredients": ["oats", "blueberries", "almond milk"],\n'
        '            "instructions": "Mix oats with almond milk, cook, and top with berries."\n'
        '          }\n'
        '        },\n'
        '        ...\n'
        '      ]\n'
        '    },\n'
        '    ...\n'
        '  ]\n'
        "}\n"
        "Only return valid JSON."
    )

    message = Content(
        role="user",
        parts=[Part(text=prompt)]
    )

    # Ensure the session exists
    async_create_session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
    )

    i = 0
    # Send message to agent and collect response
    events = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=async_create_session.id,
        new_message=message
    ):
        parts_content = event.content.parts[0].text.strip('```json').strip('```').strip()
        events = events + str(event)
 
    with open(f"./meal_plan_response_raw_again.pkl", "wb") as f:
        pickle.dump(events, f)
     
    with open(f"./meal_plan_response_parts_content.pkl", "wb") as f:
        pickle.dump(parts_content, f)
    response = json.loads(parts_content)
    return response

# Synchronous wrapper for Django views (since Django views are sync by default)
def ask_mindy_for_meal_plan(selected_foods: list[str], user_id: str = "001", session_id: str = "session_1") -> str:
    import asyncio
    import pickle
    response = asyncio.run(_ask_mindy_for_meal_plan(selected_foods, user_id, session_id))
    # Save the collected string response using pickle
    with open("./meal_plan_response.pkl", "wb") as f:
        pickle.dump(response, f)
    return response
