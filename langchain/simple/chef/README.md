# Chef AI Agent

CLI-based AI chef assistant that suggests meals from ingredients in a refrigerator photo and can answer follow-up cooking questions.

## What It Does

- Accepts a fridge image (`.jpg`, `.jpeg`, `.png`) from a local file path.
- Extracts ingredients from the image using a multimodal model.
- Uses Tavily web search to find suitable recipes.
- Keeps a short in-memory conversation thread for follow-up questions.

## Requirements

- Python `3.12+`
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

Dependencies are defined in `pyproject.toml`

## Setup

1. Move into the project:

```bash
cd langchain/simple/chef
```

2. Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

3. Install dependencies:

```bash
uv sync
```

If you do not use `uv`, install with pip instead:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
uv run python main.py
```

You can also run from an activated virtual environment:

```bash
python main.py
```

## Usage

At the prompt:

- Provide an image path:
  - `image.jpg`
  - `/full/path/to/fridge.png`
- Optionally include a text question in the same line.
- Type `exit` to quit.

If no image has been provided yet, the app will ask for one before continuing.

## Example Session

```text
> image.jpg What can I cook tonight?
...agent suggests recipes...

> I want something under 30 minutes
...agent refines the suggestions...

> exit
Goodbye
```

## Notes

- The model is currently set in `main.py` to `gpt-5-nano`.
- Conversation memory is in-process only (`InMemorySaver`) and resets when the script exits.
- Web search results are powered by Tavily via a LangChain tool wrapper.
