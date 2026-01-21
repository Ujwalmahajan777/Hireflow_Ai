from langchain_core.tools import tool
import os
import pdfplumber  # ← Move imports here, outside function

@tool
def extract_text_from_pdf(pdf_input: str = None) -> dict:
    """
    Extract text from PDF file(s). from given default folder path 
    
    Args:
        pdf_input: (Optional) Path to PDF file or folder.
                   If not provided, uses predefined path.
    
    Returns:
        dict: {filename: extracted_text} for folder,
              or {filename: text} for single file
    """
    # Define default path
    DEFAULT_RESUMES_DIR = "C:/Users/UJWAL MAHAJAN/Desktop/Hireflow_AI/Resumes"
    
    # Use provided path or default
    if pdf_input is None:
        pdf_input = DEFAULT_RESUMES_DIR
    
    # Validate path
    if not os.path.exists(pdf_input):
        return {"error": f"Path does not exist: {pdf_input}"}
    
    # Extraction logic
    result = {}
    
    if os.path.isdir(pdf_input):
        # Process directory
        for filename in os.listdir(pdf_input):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(pdf_input, filename)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"  # ← FIXED: \n not /n
                        result[filename] = text
                except Exception as e:
                    result[filename] = f"Error: {str(e)}"
    elif os.path.isfile(pdf_input) and pdf_input.lower().endswith(".pdf"):
        # Process single file
        filename = os.path.basename(pdf_input)
        try:
            with pdfplumber.open(pdf_input) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"  # ← FIXED: \n not /n
                result[filename] = text
        except Exception as e:
            result[filename] = f"Error: {str(e)}"
    else:
        return {"error": "Invalid input. Must be PDF file or directory."}
    
    return result