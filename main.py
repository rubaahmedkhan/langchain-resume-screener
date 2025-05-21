import streamlit as st
import pdfplumber
import json
import os
import smtplib
from email.message import EmailMessage
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
HR_EMAIL = os.getenv("HR_EMAIL")  # HR Email Address

# Initialize LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Prompt for Resume Screening
prompt = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template="""
    You are an expert resume screener. Extract key details from the following resume text:
    
    Resume:
    {resume_text}
    
    Compare it with the given job description:
    {job_description}
    
    Provide a structured JSON response with skills, experience, education, score, and missing skills.
    """
)

# Resume Screening Chain
resume_screener_chain = LLMChain(llm=llm, prompt=prompt)

def calculate_similarity(resume_text, job_desc):
    response = resume_screener_chain.invoke({"resume_text": resume_text, "job_description": job_desc})
    response_text = response.get("text", "{}")
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"score": 0, "missing_skills": []}

# Email Function (Updated with Debugging & Validation)
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", email)

def send_email(to_email, subject, body, attachment=None, attachment_name=None):
    if not is_valid_email(to_email):
        print("❌ Invalid email format")
        return False
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    
    if attachment and attachment_name:
        msg.add_attachment(attachment, maintype='application', subtype='pdf', filename=attachment_name)
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Email Error: {e}")
        return False

# Function to Notify HR
def notify_hr(candidate_name, resume_file):
    hr_subject = f"🎉 {candidate_name} shortlisted for Interview"
    hr_body = f"The candidate {candidate_name} has been shortlisted for an interview. Please review their application."
    resume_bytes = resume_file.getvalue()
    notify_success = send_email(HR_EMAIL, hr_subject, hr_body, attachment=resume_bytes, attachment_name=f"{candidate_name}_Resume.pdf")
    return notify_success



# Streamlit UI (Enhanced)
st.set_page_config(page_title="Resume Screening System", page_icon="📄", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("📄 Smart Resume Screening System")
st.markdown("Welcome! Upload your resume to see if you're a match for our job opening.")

st.markdown("---")

# Input Fields in Columns
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 Candidate Name")
with col2:
    email = st.text_input("📧 Candidate Email")

resume_file = st.file_uploader("📎 Upload Your Resume (PDF Only)", type=["pdf"])

st.markdown("---")

if st.button("🚀 Submit for Screening"):
    if name and email and resume_file:
        st.info("⏳ Screening your resume... please wait.")
        resume_text = extract_text_from_pdf(resume_file)
        job_description = "Looking for a Python Developer with AI expertise."
        response_data = calculate_similarity(resume_text, job_description)
        match_score = response_data.get("score", 0)
        missing_skills = response_data.get("missing_skills", [])

        st.markdown("### 📊 Screening Result")
        st.progress(int(match_score))
        st.write(f"**Match Score:** `{match_score}`")
        st.write(f"**Missing Skills:** {', '.join(missing_skills) if missing_skills else '✅ None'}")

        if match_score > 80:
            decision = "🎉 Congratulations! You have been shortlisted for an interview."
            subject = "Interview Invitation"
            notify_hr(name, resume_file)
        elif 50 <= match_score <= 79:
            decision = "✅ You have been shortlisted for future opportunities."
            subject = "Shortlist Notification"
        else:
            decision = "❌ Thank you for applying. We’ve decided to move forward with other candidates."
            subject = "Rejection Email"

            # AI Feedback
            feedback_prompt = f"Suggest skills to improve for this candidate based on missing skills: {missing_skills}"
            feedback_response = llm.invoke(feedback_prompt)
            feedback = feedback_response.get("text", "No feedback available.") if isinstance(feedback_response, dict) else feedback_response
            decision += f"\n\n🧠 **AI Feedback:**\n{feedback}"

        st.markdown("---")
        st.markdown(f"### ✉️ Decision Email Content")
        st.success(decision)

        if send_email(email, subject, decision):
            st.success(f"📧 Email successfully sent to `{email}`")
        else:
            st.error("❌ Failed to send email. Please check your credentials and try again.")
    else:
        st.warning("⚠️ Please fill in all the fields and upload your resume.")
