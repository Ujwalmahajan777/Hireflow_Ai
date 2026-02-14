# node_email_tool.py - Clean tool for your Node.js server
import requests
from datetime import datetime
from typing import Optional
from langchain.tools import tool

@tool
def schedule_interview_email(
    candidate_email: str,
    candidate_name: str,
    job_title: str,
    interview_datetime: str,
    hr_name: Optional[str] = None,
    duration_minutes: Optional[int] = None,
    interview_type: Optional[str] = None
) -> str:
    """
    Send interview email via your local Node.js email server.
    
    Args:
        candidate_email: Candidate's email address
        candidate_name: Candidate's full name
        job_title: Job position title
        interview_datetime: Date and time in format "YYYY-MM-DD HH:MM"
        hr_name: (Optional) HR manager name
        duration_minutes: (Optional) Interview duration
        interview_type: (Optional) Interview type
        
    Returns:
        str: Success or error message
    """
    try:
        # Validate required fields
        if not candidate_email:
            return "❌ candidate_email is required"
        if not candidate_name:
            return "❌ candidate_name is required"
        if not job_title:
            return "❌ job_title is required"
        if not interview_datetime:
            return "❌ interview_datetime is required"
        
        # Build request to Node.js server
        payload = {
            "candidate_email": candidate_email,
            "candidate_name": candidate_name,
            "job_title": job_title,
            "interview_datetime": interview_datetime
        }
        
        # Add optional fields if provided
        if hr_name is not None:
            payload["hr_name"] = hr_name
        if duration_minutes is not None:
            payload["duration_minutes"] = duration_minutes
        if interview_type is not None:
            payload["interview_type"] = interview_type
        
        # Send to Node.js server
        response = requests.post(
            "http://localhost:3000/send-interview-email",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Parse response
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return f"✅ Email sent: {result.get('message', 'Success')}"
            else:
                return f"❌ Server error: {result.get('error', 'Unknown error')}"
        else:
            return f"❌ HTTP {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Node.js server not running. Start it with: node server.js"
    except Exception as e:
        return f"❌ Error: {str(e)}"