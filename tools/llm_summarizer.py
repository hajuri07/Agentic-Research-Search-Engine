from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key="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")


def llm_summarizer(query: str, result):

    summarizer = []

    for r in result:
        text = f"""
Title: {r.get('title')}
Content: {r.get('content')}
URL: {r.get('url')}
"""
        summarizer.append(text)

    context = "\n".join(summarizer)

    prompt = f"""
You are an AI research assistant.

User Query: {query}

Below are retrieved results:
{context}

Task:
- Summarize key insights
- Give a clear structured answer
- Keep it concise
- Mention important sources
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt   # ✅ FIXED HERE
            }
        ]
    )

    return response.choices[0].message.content

print("GROQ KEY:", os.getenv("GROQ_API_KEY"))