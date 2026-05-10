
from tools.base_tool import BaseTool
from langchain_community.utilities import ArxivAPIWrapper
import os
import arxiv
from tools.formatter import format_response

class ArxivTool(BaseTool):

    def run(self, query):

        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []

        for paper in search.results():

            results.append({
                "title": paper.title,
                "summary": paper.summary,
                "url": paper.entry_id
            })

        return format_response("arxiv", query, results)