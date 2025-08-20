# 📄 LangChain Resume Screener

A smart AI-powered resume screening system built using **LangChain**, **Google Gemini 1.5 Flash**, and **Streamlit**. This app extracts information from resumes, compares it with job descriptions, scores the candidate, and automates email notifications to the candidate and HR.

---

## 🚀 Features

- 📤 Upload a candidate's resume (PDF)
- 📄 Extracts text using `pdfplumber`
- 🤖 Uses **Gemini LLM (via LangChain)** to:
  - Parse resume
  - Compare with job description
  - Score candidate
  - Identify missing skills
- 📧 Sends dynamic emails to:
  - The candidate (invitation, shortlist, or rejection)
  - HR (if candidate is selected)
- 💡 AI feedback for rejected candidates
- 🖥️ Clean and interactive **Streamlit UI**

---

## 🛠️ Tech Stack

- [LangChain](https://www.langchain.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- Python Standard Libraries:
  - `os`, `json`, `re`, `smtplib`, `email`




## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langchain-resume-screener.git
cd langchain-resume-screener



## Install Requirements
pip install -r requirements.txt

## Set Environment Variables
Create a .env file in the root directory:


GEMINI_API_KEY=your_google_gemini_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password_or_app_password
HR_EMAIL=hr_team_email@example.com
```

📋 How It Works
User enters their name, email, and uploads a resume.

App extracts text from PDF.

LangChain with Gemini evaluates:

Skills

Education

Experience

Score (match %)

Missing skills

Based on the score:

80: Candidate shortlisted, HR notified.

50–79: Candidate shortlisted for future.

<50: Rejected, AI suggests skill improvements.

Dynamic email is sent automatically to the candidate.


<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f50bafe0-2541-4c86-ba23-88956239b14c" />

### Demo

[Demo Link](https://huggingface.co/spaces/RubaKhan242/resume)


