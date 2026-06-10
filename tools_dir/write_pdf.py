#----------------------------------------------
# Import statements
#----------------------------------------------
from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil


@tool
def render_latex_pdf(latext_content : str) -> str:
    """
        Render a Latex Document to a PDF 

        Args:
            latex_content : The Latext Document content as a string
        
        Returns:
            Path to generated pdf doc
    """

    # Check tectonic is available or not 
    if shutil.which('tectonic') is None:      # Similar to which tectonic in the cmd 
        raise RuntimeError("tectonic is not installed. Please install it and then run it.")
    try:
        #----------------------------------------------
        # Create Directory
        #----------------------------------------------
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        #----------------------------------------------
        # Setup Filenames 
        #----------------------------------------------
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        #----------------------------------------------
        # Step : 3 - Export as tex & pdf 
        #----------------------------------------------
        # Tex Export
        tex_file = output_dir / tex_filename
        tex_file.write_text(latext_content)

        # PDF Export
        result = subprocess.run(
            ['tectonic' , tex_filename , '--outdir' , str(output_dir)],
            cwd=output_dir,
            capture_output=True,
            text=True
        )

        final_pdf = output_dir / pdf_filename
        if not final_pdf.exists():
            raise FileNotFoundError("PDF file was not generated")
        print(f"Sucessfully  Generated PDF at {final_pdf}")
        return str(final_pdf)
    except Exception as e:
        print("Error in write PDf render_latex_pdf function")
        print(str(e))



# sample_latex_data = r"""
# \documentclass{article} 
# \begin{document}
# Hello, world! From LaTex to PDF with Python.
# \end {document}
# """

# render_latex_pdf(latext_content=sample_latex_data)