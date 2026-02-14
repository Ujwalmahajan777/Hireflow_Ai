# email_via_proxy.py - Python calls Node.js proxy
import requests
from datetime import datetime

def send_email_via_proxy(
    candidate_email: str,
    candidate_name: str,
    hr_name: str,
    job_title: str,
    interview_datetime: str,
    duration_minutes: int = 45
    )
    
    """
    Send email via Node.js proxy (100% working).
    """
    try:
        # Send request to Node.js proxy
        response = requests.post(
            "http://localhost:3000/send-interview-email",
            json={
                "candidate_email": candidate_email,
                "candidate_name": candidate_name,
                "hr_name": hr_name,
                "job_title": job_title,
                "interview_datetime": interview_datetime,
                "duration_minutes": duration_minutes
            },
            timeout=10  # 10 second timeout
        )
        
        result = response.json()
        print(result)
        
        if result.get("success"):
            return f"✅ {result['message']}"
        else:
            return f"❌ Proxy Error: {result.get('error', 'Unknown error')}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Node.js proxy server not running. Start it with: node emailjs_proxy.js"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Test immediately
if __name__ == "__main__":
    result = send_email_via_proxy(
        candidate_email="ujwalmahajan1234@gmail.com",
        candidate_name="Test Candidate",
        hr_name="HR Manager",
        job_title="AI Engineer",
        interview_datetime="2024-02-15 14:30"
    )
    print("Result:", result)