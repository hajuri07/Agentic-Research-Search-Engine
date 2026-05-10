
from tools.tavily_tools import TavilyTool
from tools.firecrawl_tool import FireCrawl
from tools.arxiv_tools import ArxivTool

class ToolManager:

    def __init__(self):

        self.tools = {
            "search": TavilyTool(),
            "jobs": FireCrawl(),
            "papers": ArxivTool()
        }

    def use_tool(self, tool_name: str, query: str):

        tool = self.tools.get(tool_name)

        if not tool:
            print("AVAILABLE TOOLS:", self.tools.keys())
            print("REQUESTED TOOL:", tool_name)
            return {"results": [],
                    "error": "Tool not found",
                    
                    }

        return tool.run(query)