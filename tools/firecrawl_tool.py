from firecrawl import FirecrawlApp
from tools.base_tool import BaseTool
import os

from dotenv import load_dotenv
load_dotenv()

class FireCrawl(BaseTool):
    
    def __init__(self):
        self.app=FirecrawlApp(api_key= "fc-f25d505848b3472985e3627ad8fadda3")

    def run(self,query:str):

        response = self.app.search(
            query=query,
            limit=5,
            scrape_options={
                "formats":["markdown"]
            }
        )
        
        cleaned=[]

        for item in response["data"]:
            cleaned.append({"title":item.get("title"),
                "url":item.get("url"),
                "description":item.get("description")
                })
            
        return cleaned 

