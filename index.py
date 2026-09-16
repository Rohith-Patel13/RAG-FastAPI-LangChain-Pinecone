
# https://fastapi.tiangolo.com/tutorial/body/

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
load_dotenv()

from langchain.agents import create_agent
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

# --- Pinecone + embeddings setup (created once when the server starts) ---
# The query MUST be embedded with the same model/size used to build the index:
# gemini-embedding-001 at 768 dimensions (test-index is 768-dim, cosine).
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    output_dimensionality=768,
)
pinecone_index = Pinecone().Index("test-index")


# The triple-quoted string right below a function is a "docstring". It is NOT a
# comment (# is a comment). LangChain reads this docstring and sends it to the LLM
# as the tool's description, so the model knows what the tool does and when to call
# it. If you use a # comment instead, LangChain sees no description and errors out.
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


def search_knowledge_base(query: str) -> str:
    """Search the private knowledge base for information about specific people,
    students, clubs, or the University of Washington. Use this whenever the user
    asks about a named person (for example Alexandra) or details that would be
    stored in our records, rather than general world knowledge."""
    query_vector = embeddings.embed_query(query)
    results = pinecone_index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True,
    )
    matches = results.matches
    if not matches:
        return "No relevant information found in the knowledge base."
    print("Matches found in knowledge base:", matches)  # Python uses print(), not console.log()
    return "\n\n".join(m.metadata["document"] for m in matches)


agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[get_weather, search_knowledge_base],
    system_prompt=(
        "You are a helpful assistant. "
        "When the user asks about specific people, students, clubs, or the "
        "University of Washington, call the search_knowledge_base tool and answer "
        "using what it returns. For general questions, answer directly from your "
        "own knowledge without calling any tool."
    ),
)


class Chat(BaseModel):
    question: str


app = FastAPI()


# The "@" makes this a decorator. @app.post("/chat/") registers the function below
# as the handler for POST requests to the /chat/ path. You never call create_chat
# yourself; FastAPI calls it automatically when a matching request arrives.
# (Like Express's app.post("/chat/", handler) in Node, just attached with @ instead
# of passed as an argument.)
@app.post("/chat/")
async def create_chat(chat: Chat):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": chat.question}]}
    )
    return {"reply": result["messages"][-1].content}


# --- How to run this app ---
# Run the command below in the terminal (with the venv activated):
#
#     uvicorn index:app --reload
#
#   uvicorn  -> the web server that runs FastAPI apps and keeps listening for requests
#   index    -> this file, index.py (without the .py)
#   app      -> the FastAPI() object above (app = FastAPI())
#   --reload -> auto-restart the server whenever this file is saved (for development)
#
# Do NOT use `python index.py` for a FastAPI app: that just defines everything and
# exits without serving. uvicorn loads the app and stays running so the endpoint can
# be called. Server starts at http://127.0.0.1:8000 (interactive docs at /docs).
