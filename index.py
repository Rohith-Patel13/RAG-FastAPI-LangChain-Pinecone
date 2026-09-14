
# https://fastapi.tiangolo.com/tutorial/body/

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
load_dotenv()
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

class Chat(BaseModel):
    question: str

app = FastAPI()


@app.post("/chat/")
async def create_chat(chat: Chat):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": chat.question}]}
    )
    return result["messages"][-1].content_blocks
