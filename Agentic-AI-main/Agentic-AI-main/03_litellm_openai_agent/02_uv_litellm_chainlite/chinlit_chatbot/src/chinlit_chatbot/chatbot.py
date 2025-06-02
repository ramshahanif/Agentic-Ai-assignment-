import os
from dotenv import load_dotenv
import chainlit as cl 
from litellm import completion
import json

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set.Please ensure it is defined in your .env file")

@cl.on_chat_start
async def start():
    cl.user_session.set("Chat_history" , [])
    await cl.Message(content= "🤖 Welcome to the RSK AI Assisatant.How can i help you today?")

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content = "🤔Thinking")
    await msg.send()
    history = cl.user_session.get("Chat_history" or [])
    history.append({"role":"user","content":message.content})
    try:
        response = completion(
            model="openrouter/mistralai/devstral-small:free",
            api_key = OPENROUTER_API_KEY,
            base_url = BASE_URL,
            messages = history
        )
        response_content = response.choices[0].message.content
        msg.content = response_content
        await msg.update()
        history.append({"role":"user","content":response_content})
        cl.user_session.set("Chat_history",history)
        print(f'User: {msg_content}')
        print(f'RSK AI Assistant: {response_content}')

    except Exception as e:
        message.content = f'Error: {str(e)}'
        await msg.update()
        print(f'Error: {str(e)}')

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("Chat_history" or [])
    with open("Chat_history.json","w") as f:
        json.dump(history,f,indent=2)
    print("Chat history saved.")

if __name__ == "__main__":
    print("✅ Chainlit app file is being run directly.")
    print("📢 Start the app using: chainlit run your_file.py")