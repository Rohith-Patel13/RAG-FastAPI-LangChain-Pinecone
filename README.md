# RAG-FastAPI-LangChain-Pinecone

A Retrieval-Augmented Generation (RAG) service built with **FastAPI**, **LangChain**, and **Pinecone**.

## Prerequisites

- Python 3.12+
- `pip` (comes with Python)

## Setup

> **Note for Node.js developers:** Python has no `package.json`. Packages install into a
> _virtual environment_ (the equivalent of `node_modules`), and dependencies are tracked
> manually in `requirements.txt`. The steps below set that up.

### 1. Create a virtual environment

This creates an isolated, project-local Python environment in a `venv/` folder:

```bash
python -m venv venv
```

- `python -m venv` runs Python's built-in `venv` module.
- The second `venv` is the folder name to create (a common convention).

### 2. Activate the virtual environment

**Git Bash / MINGW64 (Windows):**

```bash
source venv/Scripts/activate
```

**PowerShell (Windows):**

```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

Once active, your prompt shows `(venv)`. Now `pip install` puts packages inside `venv/`
instead of your global/user Python.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install fresh and record them:

```bash
pip install langchain langchain-google-genai fastapi "uvicorn[standard]" python-dotenv pinecone
pip freeze > requirements.txt
```

> **Vector search:** the app uses the `pinecone` client directly. Queries are embedded with
> Google's `gemini-embedding-001` model at **768 dimensions** to match the `test-index`
> (768-dim, cosine). The stored text lives in each record's `document` metadata field.

`requirements.txt` is this project's dependency list (the `package.json` equivalent).
Commit it so others can rebuild the same environment.

> **Note:** `langchain-google-genai` is the wrapper for the Google **AI Studio (Gemini API)**
> path — the one that uses a simple API key. The model is prefixed `google_genai:` in code so
> LangChain uses this path instead of Vertex AI (which would need a Google Cloud project).

### 4. Configure environment variables

Create a `.env` file in the project root (it is gitignored) with your Gemini API key
from [Google AI Studio](https://aistudio.google.com/apikey):

```
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_pinecone_key_here
```

The app loads these automatically via `load_dotenv()` in `index.py`.
Get the Pinecone key from your [Pinecone console](https://app.pinecone.io/) → API keys.

## How it works (RAG via tools)

The agent has two tools and decides which to use per question:

- **`search_knowledge_base`** — embeds the question and does a vector search against the
  Pinecone `test-index`. Used for questions about stored people/records (e.g. "Tell me about
  Alexandra").
- **`get_weather`** — a demo tool.

General questions (e.g. "What is the capital of France?") are answered directly by the LLM,
with no tool call. This routing is driven by each tool's docstring plus the agent's system
prompt — you don't call the vector search manually.

### 5. Deactivate when done

```bash
deactivate
```

## Running the app

This is a FastAPI app, so run it with the **uvicorn** server (not `python index.py`,
which would just set up the app and exit without serving requests):

```bash
uvicorn index:app --reload
```

- `index` = the file `index.py`
- `app` = the `FastAPI()` object inside it
- `--reload` = auto-restart on code changes (development)

The server starts at **http://127.0.0.1:8000** and stays running (Ctrl+C to stop).

### Testing the endpoint

The app exposes a `POST /chat/` endpoint that takes a question and returns the agent's reply.

**Option A — interactive docs (built in):** open **http://127.0.0.1:8000/docs**, expand
`POST /chat/`, click *Try it out*, and send a request.

**Option B — Postman / curl:**

- Method: `POST`
- URL: `http://127.0.0.1:8000/chat/`  _(keep the trailing slash)_
- Body → raw → JSON:

```json
{
  "question": "What's the weather in San Francisco?"
}
```

curl equivalent:

```bash
curl -X POST http://127.0.0.1:8000/chat/ -H "Content-Type: application/json" -d "{\"question\": \"What's the weather in San Francisco?\"}"
```

> Note: visiting `http://127.0.0.1:8000/` in a browser returns **404** — that's expected.
> Browsers send `GET`, and there is no `GET /` route; only `POST /chat/` is defined.

## Managing packages

| Task | Command |
|---|---|
| Install a package | `pip install <name>` |
| Uninstall a package | `pip uninstall <name>` |
| See where a package lives | `pip show <name>` |
| List installed packages | `pip list` |
| Save current deps | `pip freeze > requirements.txt` |

## Notes

- Always activate the venv before installing or running anything.
- `pip uninstall <name>` removes only that package, **not** its dependencies.
- Add `venv/` to your `.gitignore` — never commit the environment itself.
