
#----------------------------------------------
# Import Statements
#----------------------------------------------

from langchain_core.tools import tool 
import io 
import PyPDF2
import requests
# url = "https://arxiv.org/pdf/2606.11182v1"

@tool
def read_pdf(url : str) -> str:
    """
    Download a PDF from a URL and extract text from all pages.

    Args:
        url (str): Direct URL to the PDF file.

    Returns:
        str: Combined text extracted from the PDF.
    """
    try:
        # Step : 1 - Access PDF With URL
        response = requests.get(url=url)

        # Step : 2 - Convert to Bytes

        pdf_file = io.BytesIO(response.content)

        # Step : 3 - Retrive Text from PDF

        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Step : 4 - Extract text from all pages
        text = ""
        for i,page in enumerate(pdf_reader.pages , 1):
            print(f"Extracting for page {i}/{num_pages}")
            text += page.extract_text() + "\n"

        print(f"Successfully Extracted {len(text)} words of text from PDF")

        return text.strip()
    
    except Exception as e:
        print("Error in reading pdf -> read_pdf")
        print(str(e))

