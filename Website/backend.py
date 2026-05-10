from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import time
import tools.tool_manager
from tools.llm_summarizer import llm_summarizer
from tools.tool_router import ToolRouter

app = FastAPI()

manager = tools.tool_manager.ToolManager()
router = ToolRouter()

@app.get("/search-stream")
def search_stream(query: str):

    def generate():

        
        yield json.dumps({
            "status": "started"
        }) + "\n"

        
        selected_tool = router.route(query)

        yield json.dumps({
            "status": "tool_selected",
            "tool": selected_tool
        }) + "\n"

        
        result = manager.use_tool(selected_tool, query)

        print("FULL RESULT:", result)
        print("RESULT TYPE:", type(result))

        
        results = result.get("results", [])

        
        yield json.dumps({
            "status": "processing"
        }) + "\n"

        
        for item in results:

            print("ITEM:", item)
            print("ITEM TYPE:", type(item))

           
            if not isinstance(item, dict):
                print("INVALID ITEM SKIPPED")
                continue

            yield json.dumps({
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "url": item.get("url", "")
            }) + "\n"

            time.sleep(0.3)

        # generate summary
        summary = llm_summarizer(query, results)

        yield json.dumps({
            "status": "summary",
            "summary": summary
        }) + "\n"

        
        yield json.dumps({
            "status": "done"
        }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )


@app.get("/search")
def search(query: str):

    try:

        # route tool
        selected_tool = router.route(query)

        # retrieve results
        result = manager.use_tool(selected_tool, query)

        # safe extraction
        results = result.get("results", [])

        # llm summary
        summary = llm_summarizer(query, results)

        # final response
        return {
            "status": "success",
            "query": query,
            "tool_used": selected_tool,
            "results": results,
            "summary": summary
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
            "results": []
        }