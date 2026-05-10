

def format_response(source: str, query: str, results: list):

    cleaned = []

    for item in results:
        cleaned.append({
            "title": item.get("title"),
            "content": item.get("summary") or item.get("description") or "",
            "url": item.get("url"),
            "type": "paper" if source == "arxiv" else "web"
        })

    return {
        "source": source,
        "query": query,
        "results": cleaned
    }