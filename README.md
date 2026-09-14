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
pip install langchain fastapi "uvicorn[standard]" pinecone
pip freeze > requirements.txt
```

`requirements.txt` is this project's dependency list (the `package.json` equivalent).
Commit it so others can rebuild the same environment.

### 4. Deactivate when done

```bash
deactivate
```

## Running the app

```bash
uvicorn index:app --reload
```

_(Adjust `index:app` to match your FastAPI app object.)_

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
