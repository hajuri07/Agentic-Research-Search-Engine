from tool_manager import ToolManager
from llm_summarizer import llm_summarizer
from pathlib import Path
from dotenv import load_dotenv
import os

# Load env safely
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

manager = ToolManager()

# input
query = input("Enter your query: ")

print("\n🔍 Running tool...\n")

tool = "arxiv"

result = manager.use_tool(tool, query)

print("\nDEBUG TYPE:", type(result))
print("DEBUG VALUE:", result)

results_list = result.get("results", [])

print(f"\n📦 Retrieved {len(results_list)} results")

print("\n🧠 Sending to LLM summarizer...\n")

summary = llm_summarizer(query, results_list)

print("\n🔥 FINAL OUTPUT:\n")
print(summary)