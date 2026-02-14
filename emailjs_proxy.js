// run command "nodemon"

import express from "express"
import cors from "cors";
import axios from 'axios';
import dotenv from "dotenv"

const app = express();
app.use(cors());
app.use(express.json());

dotenv.config();

const EMAILJS_CONFIG = {
    serviceId: process.env.EMAILJS_SERVICE_ID,     
    templateId: process.env.EMAILJS_TEMPLATE_ID,    
    userId: process.env.EMAILJS_PUBLIC_KEY          
};

// Test endpoint
app.get('/', (req, res) => {
    res.json({ 
        status: 'running',
        message: 'EmailJS Proxy Server - Fixed Version',
        endpoints: {
            test: 'GET /test',
            send: 'POST /send-interview-email'
        }
    });
});

// Quick test endpoint
app.get('/test', async (req, res) => {
    try {
        const response = await axios.post(
            'https://api.emailjs.com/api/v1.0/email/send',
            {
                service_id: EMAILJS_CONFIG.serviceId,
                template_id: EMAILJS_CONFIG.templateId,
                user_id: EMAILJS_CONFIG.userId,
                template_params: {
                    to_email: 'ujwalmahajan1234@gmail.com',
                    test_param: 'Test Value'
                }
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'origin': 'http://localhost:3000'  // Important!
                }
            }
        );
        
        res.json({ 
            success: true, 
            message: 'Test email sent!',
            response: response.data 
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.response?.data || error.message
        });
    }
});

// Main email sending endpoint
app.post('/send-interview-email', async (req, res) => {
    try {
        const {
            candidate_email,
            candidate_name,
            hr_name,
            job_title,
            interview_datetime,  // Format: "2024-02-15 14:30"
            duration_minutes = 45,
            interview_type = "Video Call"
        } = req.body;

        console.log('📧 Processing email for:', candidate_name);

        // Parse and format date
        const [datePart, timePart] = interview_datetime.split(' ');
        const [year, month, day] = datePart.split('-').map(Number);
        const [hour, minute] = timePart.split(':').map(Number); 
        
        const interviewDate = new Date(year, month - 1, day, hour, minute);
        
        // Format date for display
        const formattedDate = interviewDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const formattedTime = interviewDate.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });

        // Template parameters - MUST match your EmailJS template variables
        const templateParams = {
            to_email: candidate_email || "ujwalmahajan1234@gmail.",
            company_name: 'Hireflow AI',
            job_title: job_title || "Gen AI Engineer",
            candidate_name: candidate_name ||"ujwal mahajan",
            interview_date: formattedDate,      // "February 15, 2024"
            interview_time: formattedTime,      // "02:30 PM"  
            timezone: 'IST',
            duration_minutes: duration_minutes.toString()|| "2 hours",
            interview_type: interview_type || "technical round",
            hr_name: hr_name || "ujwal patil",
            hr_email: 'hr@hireflow-ai.com',
            hr_phone: '+91 9876543210',
            company_website : "www.hireflow.com",
            company_address : "Ashoknagar , Satpur Colony, Nashik"
        };

        console.log('📝 Template params:', templateParams);

        // Send email via EmailJS API
        const response = await axios.post(
            'https://api.emailjs.com/api/v1.0/email/send',
            {
                service_id: EMAILJS_CONFIG.serviceId,
                template_id: EMAILJS_CONFIG.templateId,
                user_id: EMAILJS_CONFIG.userId,
                template_params: templateParams
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'origin': 'http://localhost:3000',  // Required for CORS
                    'User-Agent': 'Node.js Proxy Server'
                }
            }
        );
        

        console.log('✅ Email sent successfully:', response.data);

        res.json({
            success: true,
            message: `Email sent to ${candidate_name}`,
            emailId: response.data,
            templateUsed: templateParams
        });

    } catch (error) {
        console.error('❌ Email error:', error.response?.data || error.message);
        
        res.status(500).json({
            success: false,
            error: error.response?.data || error.message,
            details: 'Check your EmailJS credentials and template variables'
        });
    }
}); 

// Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`\n🚀 EmailJS Proxy Server (FIXED) running on http://localhost:${PORT}`);
});