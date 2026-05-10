class ToolRouter:

    def route(self, query: str):

        query = query.lower()

        # research papers
        if any(word in query for word in [
            "paper",
            "research",
            "arxiv",
            "study",
            "llm paper"
        ]):
            return "arxiv"

        # jobs / scraping
        elif any(word in query for word in [
            "job",
            "hiring",
            "career",
            "salary"
        ]):
            return "firecrawl"

        # default web search
        else:
            return "tavily"