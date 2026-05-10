from abc import abstractmethod
from urllib import response
from tools.formatter import format_response
from tavily import TavilyClient
from tools.base_tool import BaseTool
import os
from dotenv import load_dotenv
load_dotenv()

class TavilyTool(BaseTool):
    def __init__(self):
        self.tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        
    def run(self,query:str):
            response = self.tavily.search(query=query,search_depth="advanced")
            
            results=[]
            for item in response["results"]:
                results.append({
                    "title":item["title"],
                    "url":item["url"],
                    "content":item["content"]})
            return format_response("tavily", query, response["results"])
        
           
