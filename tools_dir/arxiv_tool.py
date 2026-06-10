#----------------------------------------------
# Import Statements
#----------------------------------------------

import requests 
import xml.etree.ElementTree as ET
from langchain_core.tools import tool

#----------------------------------------------
# Step : 1 - Access ArXiv using URL
#----------------------------------------------

def search_arxiv_papers(topic : str , max_results : int = 5) -> dict: 
    
    """
    Search arXiv for papers on a given topic and return parsed results.

    Args:
        topic (str): Search keyword or topic.
        max_results (int): Maximum number of papers to retrieve.

    Returns:
        dict: Parsed arXiv paper metadata.
    """
    
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            print(f"Invalid Character '{char} in query: {query}")
            raise ValueError(f"Cannot have character : '{char}' in query : '{query}'")


    url = (
                "http://export.arxiv.org/api/query"
                f"?search_query=all:{query}"
                f"&max_results={max_results}"
                "&sortBy=submittedDate"
                "&sortOrder=descending"
        )
    print("Making Request to ArXiv Api : " , url)
    response = requests.get(url=url)
    if not response.ok:
        print(f"ArXiv Api request fail : {response.status_code} - {response.text}")
        raise ValueError(f"Bad response from arXiv Api : {response}\n{response.text}")
    
    data = parse_arxiv_xml(response.text)
    return data


#----------------------------------------------
# Step : 2 - Parse XML data
#----------------------------------------------


def parse_arxiv_xml(xml_content : str) -> dict:
    
    """
    Parse an arXiv XML response and extract paper metadata.

    Args:
        xml_content (str): Raw XML content from the arXiv API.

    Returns:
        dict: Dictionary containing a list of paper entries with
        title, summary, authors, categories, and PDF link.
    """

    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)

    # Loop through each <entry> in Atom Namespace
    for entry in root.findall("atom:entry" , ns):
        
        # Extract Authors
        authors = [
            author.findtext("atom:name" , namespaces=ns) for author in entry.findall("atom:author" , ns)
        ]

        # Extract Categories 
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category" , ns)
        ]

        # Extract PDF Link 
        pdf_link = None
        for link in entry.findall("atom:link" , ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break 
        
        # Appending to main entries
        entries.append({
            "title" : entry.findtext("atom:title" , namespaces=ns),
            "summary" : entry.findtext("atom:summary" , namespaces=ns).strip(),
            "authors" : authors,
            "categories" : categories,
            "pdf_link" : pdf_link
        })

    return {'entries' : entries}


#----------------------------------------------
# Step : 3 - Convert the functionality in a tool
#----------------------------------------------

@tool
def arxiv_search(topic : str) -> list[dict]:

    """
    Search arXiv for recent uploaded papers on a topic and return the results.

    Args:
        topic (str): Topic to search for.

    Returns:
        list[dict]: Matching paper entries.

    Raises:
        ValueError: If no papers are found.
    """
    
    print("arXiv Agent Called")
    print(f"Searching arXiv for papers about: {topic}")
    papers = search_arxiv_papers(topic)
    if len(papers) == 0:
        print(f"No papers found for topic {topic}")
        raise ValueError(f"No papers found for topic: {topic}")
    print(f"Found {len(papers['entries'])} papers about {topic}")
    return papers 