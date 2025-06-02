import asyncio
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_disabled
from dotenv import load_dotenv
from agents.run import RunConfig
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-prover-v2:free"

client = AsyncOpenAI(api_key = OPENROUTER_API_KEY, base_url = BASE_URL)

config = RunConfig(
    model = MODEL
    model_provider = client
    tracing_disabled= True
)
async def main():
    agent = Agent(
        name= "Chat bot",
        instructions = "You are a helpful assistant who answers clearly and briefly",
        model = OpenAIChatCompletionsModel(model=MODEL,openai_client = client)
    )
    print("🤖 RSK BOT is ready. Type 'exit' to quit.\n", run_config=config)
 
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        result = await Runner.run(agent, user_input)
        print("Assistant:", result.final_output)

    

if __name__ == "__main__":
    asyncio.run(main())