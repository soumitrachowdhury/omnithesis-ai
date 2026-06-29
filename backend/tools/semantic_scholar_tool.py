import os
import requests
from crewai.tools import tool

@tool("search_semantic_scholar")
def search_semantic_scholar(query: str) -> str:
    """
    Searches Semantic Scholar for academic papers.
    Useful for finding real research papers on a given topic.
    Returns a formatted string containing paper titles, authors, published dates, and summaries.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    # MISTAKE #6: Handle optional API key so development isn't blocked
    headers = {}
    if os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        
    params = {
        "query": query,
        "limit": 5,
        "fields": "title,authors,year,abstract,url"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "data" not in data or not data["data"]:
            return "No papers found on Semantic Scholar for this query."
            
        results = []
        for paper in data["data"]:
            paper_info = f"Title: {paper.get('title', 'N/A')}\n"
            authors = [author.get('name', 'Unknown') for author in paper.get('authors', [])]
            paper_info += f"Authors: {', '.join(authors)}\n"
            paper_info += f"Published: {paper.get('year', 'N/A')}\n"
            paper_info += f"Link: {paper.get('url', 'N/A')}\n"
            paper_info += f"Summary: {paper.get('abstract', 'N/A')}\n"
            results.append(paper_info)
            
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error searching Semantic Scholar: {str(e)}"
