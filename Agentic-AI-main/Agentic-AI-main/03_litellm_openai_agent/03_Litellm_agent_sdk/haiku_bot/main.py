import os
from dotenv import load_dotenv
from agents import Agent, function_tool, Runner
from agents.extensions.models.litellm_model import LitellmModel 
import chainlit as cl 

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/meta-llama/llama-3.3-8b-instruct:free"

@function_tool
def get_weather(city:str)->str:
    return f'The weather of {city} is bright and calm'

agent = Agent(
    name = "Weather Bot",
    instructions = "You only respond in haikus.",
    model = LitellmModel(
        model = MODEL,
        base_url = BASE_URL,
        api_key = OPENROUTER_API_KEY
    ),
    tools = [get_weather]
)

@cl.on_chat_start
async def start():
    await cl.Message(content = "🌤️ Welcome to the Weather Bot! Ask me anything...").send()

@cl.on_message
async def on_message(message:cl.Message):
    msg = cl.Message(content = "🔍 Searching")
    await msg.send()
    try:
        result = await Runner.run(agent, message.content)
        msg.content = result.final_output
        await msg.update()
    except Exception as e:
        msg.content = f'Error: {str(e)}'
        await msg.update()

