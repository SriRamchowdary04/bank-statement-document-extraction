import os
from dotenv import load_dotenv

load_dotenv()

INPUT_DIR = os.getenv("INPUT_DIR", "data/input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/output")

LLM_PROVIDERS = [
    x.strip().lower()
    for x in os.getenv("LLM_PROVIDERS", "openai").split(",")
    if x.strip()
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
