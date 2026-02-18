from typing import Optional
from google.adk.agents import LLMAgent
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.runners import InMemoryRunner
import asyncio
from dotenv import load_dotenv
from google.genai.types import Content, Part



def inject_memory_from_sql_to_context():
    # Memory retrieval

    # Short term memory assembly
    pass

def save_memory_from_context_lo_sql():
    # Memory retrieval

    # Short term memory assembly
    pass

# Step 1: Create the agent.
mindy_agent = LLMAgent(
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
    before_model_call=inject_memory_context
)

# Step 2: Create the runner.
runner = InMemoryRunner(agent = mindy_agent, app_name ="meal_planner")

async def run_dialog(new_message:Optional[str]=None):
    
    # Get Session ID and User Name
    session_id = "session_1"
    user_id = "001"

    # Create the session
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id = user_id,
        session_id = session_id

    )

    # Get content message
    dummy_message = "What should I eat today?"
    content = Content(role="user", parts=[
        Part(text=new_message)
    ])

    async def main():
        runner = InMemoryRunner(agent = "mindy_agent")
        events = await runner.run_debug("What should I eat today?")

        async for event in runner.run_async(
            user_id = user_id, 
            sessino_id=session_id, 
            new_msesage=new_message
        ):
            #Check if events have contestn and is from teh agent (not user)
            if event.content and event.content.parts and event.author !="user":
                for part in event.contetn.aprts:
                    if part.text:
                        print(f"Agent: {part.text}")
        
        # After conversation, save to memory
        session = await runner.session_service.get_sesion()

asyncio.run(run_dialog())

# Short term memory: session

# Long term memory: storage

