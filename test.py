# test_emailjs_simple.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the pure function directly (no LangChain)
from email_via_proxy import send_interview_email_pure

result = send_interview_email_pure(
    candidate_email="ujwalmahajan1234@gmail.com",  # Your email
    candidate_name="Test Candidate",
    hr_name="HR Manager",
    job_title="AI Engineer",
    interview_datetime="2024-02-15 14:30",
    duration_minutes=45
)

print("Test Result:", result)
print("\nCheck your inbox and spam folder!")