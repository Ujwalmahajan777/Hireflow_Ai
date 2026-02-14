from langchain_core.tools import tool
import os
import pdfplumber  # ← Move imports here, outside function
from langsmith import traceable


@tool
@traceable(name = "extract text from resumes",tags=["dimension:resume text"],metadata={"dimension":"resumetext"})
def extract_text_from_pdf(pdf_input: str = None) -> dict:
    """
    Extract text from PDF file(s). from given default folder path 
    
    Args:
        pdf_input: (Optional) Path to PDF file or folder 
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


# import os
# import resend
# from datetime import datetime
# from dotenv import load_dotenv
# from langchain.tools import tool
# from email_template import INTERVIEW_SCHEDULED_TEMPLATE

# load_dotenv()
# resend.api_key = os.getenv("RESEND_API_KEY")

# @tool
# def send_interview_email(
#     candidate_email: str,
#     candidate_name: str,
#     hr_name: str,
#     job_title: str,
#     interview_datetime: str,
#     duration_minutes: int = 45
# ) -> str:
#     """
#     Send interview scheduled email to candidate using Resend service.
#     """
#     try:
#         # Parse datetime and format for email
#         dt = datetime.strptime(interview_datetime, "%Y-%m-%d %H:%M")
#         interview_date = dt.strftime("%B %d, %Y")
#         interview_time = dt.strftime("%I:%M %p")

#         # Fill the template (from your email_templates.py)
#         subject = INTERVIEW_SCHEDULED_TEMPLATE["subject"].format(job_title=job_title)
#         html_body = INTERVIEW_SCHEDULED_TEMPLATE["html_body"].format(
#             candidate_name=candidate_name,
#             job_title=job_title,
#             interview_date=interview_date,
#             interview_time=interview_time,
#             duration_minutes=duration_minutes,
#             hr_name=hr_name
#         )

#         # Send email via Resend
#         r = resend.Emails.send({
#         # Use Resend's allowed test domain
#         "from": "Hireflow AI <onboarding@resend.dev>",
        
#         # CRITICAL: Send ONLY to your own email address for testing
#         # Replace this with the exact email you used to sign up for Resend
#         "to": ["ujwalmahajan1234@gmail.com"],
        
#         "subject": subject,
#         "html": html_body,
        
#         # Optional: Add a text version (good practice)
#         "text": f"""Dear {candidate_name},

#         Your interview for the {job_title} position has been scheduled.

#         Date: {interview_date}
#         Time: {interview_time}
#         Duration: {duration_minutes} minutes
#         Interviewer: {hr_name}

#         Best regards,
#         HR Team"""
#         })

#         return f"✅ Email sent successfully to {candidate_name}. Email ID: {r['id']}"

#     except ValueError:
#         return "❌ Error: Invalid datetime format. Use 'YYYY-MM-DD HH:MM'."
#     except Exception as e:
#         return f"❌ Error sending email: {str(e)}"

# tools.py - Only wraps the pure function
