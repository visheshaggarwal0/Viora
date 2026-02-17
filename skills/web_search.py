from langchain_community.tools import DuckDuckGoSearchRun

class WebSearch:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def run(self, query: str):
        """Performs a web search using DuckDuckGo."""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"
