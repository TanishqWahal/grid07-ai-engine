from langchain.tools import tool

@tool
def mock_searxng_search(query: str):
    """Search for recent news based on a query."""   

    if "AI" in query:
        return "New AI model replacing junior developers"
    elif "crypto" in query:
        return "Bitcoin hits all-time high"
    elif "market" in query:
        return "Stock market shows volatility"
    return "No major news found"
