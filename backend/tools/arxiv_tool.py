import arxiv
from crewai.tools import tool

@tool("search_arxiv")
def search_arxiv(query: str) -> str:
    """
    Searches the ArXiv database for academic papers.
    Useful for finding real research papers on a given topic.
    Returns a formatted string containing paper titles, authors, published dates, and summaries.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in client.results(search):
            paper_info = f"Title: {result.title}\n"
            paper_info += f"Authors: {', '.join([author.name for author in result.authors])}\n"
            paper_info += f"Published: {result.published.strftime('%Y-%m-%d')}\n"
            paper_info += f"Link: {result.pdf_url}\n"
            paper_info += f"Summary: {result.summary}\n"
            results.append(paper_info)
            
        if not results:
            return "No papers found on ArXiv for this query."
            
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error searching ArXiv: {str(e)}"
