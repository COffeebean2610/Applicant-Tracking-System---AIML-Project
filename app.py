from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def generate_pdf_report(analysis_type, response, job_description, resume_filename):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30)
    story.append(Paragraph("ATS Resume Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Report Info
    info_style = styles['Normal']
    story.append(Paragraph(f"<b>Analysis Type:</b> {analysis_type}", info_style))
    story.append(Paragraph(f"<b>Resume File:</b> {resume_filename}", info_style))
    story.append(Paragraph(f"<b>Generated On:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
    story.append(Spacer(1, 20))
    
    # Job Description
    story.append(Paragraph("<b>Job Description:</b>", styles['Heading2']))
    story.append(Paragraph(job_description[:500] + "..." if len(job_description) > 500 else job_description, info_style))
    story.append(Spacer(1, 20))
    
    # Analysis Results
    story.append(Paragraph("<b>Analysis Results:</b>", styles['Heading2']))
    story.append(Paragraph(response, info_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

# Landing Page
st.title("🎯 ATS Resume Expert - AI-Powered Resume Analysis")
st.markdown("---")

# Project Overview
with st.expander("📋 What is this project about?", expanded=True):
    st.markdown("""
    **ATS Resume Expert** is an intelligent resume analysis tool that leverages Google's Gemini Pro Vision AI model 
    to evaluate resumes against job descriptions. It simulates how Applicant Tracking Systems (ATS) scan and 
    score resumes, helping job seekers optimize their applications for better visibility to recruiters.
    
    The system analyzes PDF resumes using computer vision and natural language processing to provide:
    - Professional resume evaluation
    - Percentage match scoring
    - Missing keywords identification
    - Improvement recommendations
    """)

# Technologies Used
with st.expander("🛠️ Technologies & Libraries Used"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Technologies:**
        - **Python** - Main programming language
        - **Streamlit** - Web application framework
        - **Google Gemini Pro Vision** - AI model for analysis
        - **PIL (Pillow)** - Image processing
        - **pdf2image** - PDF to image conversion
        """)
    
    with col2:
        st.markdown("""
        **Additional Libraries:**
        - **python-dotenv** - Environment variable management
        - **base64** - Data encoding
        - **io** - Input/output operations
        - **os** - Operating system interface
        - **reportlab** - PDF report generation
        """)

# How it's Made
with st.expander("⚙️ How it's Made"):
    st.markdown("""
    **Architecture & Workflow:**
    
    1. **PDF Processing**: Converts uploaded PDF resume to JPEG image using pdf2image
    2. **Image Encoding**: Encodes image to base64 format for API transmission
    3. **AI Analysis**: Sends job description and resume image to Google Gemini Pro Vision
    4. **Response Generation**: AI analyzes content and provides detailed feedback
    5. **Results Display**: Presents analysis in user-friendly format
    
    **Key Components:**
    - `get_gemini_response()`: Handles AI model communication
    - `input_pdf_setup()`: Processes PDF files for analysis
    - Streamlit UI: Provides interactive web interface
    """)

# How to Use
with st.expander("📖 How to Use - Step by Step Guide"):
    st.markdown("""
    **Step 1:** Prepare your materials
    - Have your resume in PDF format ready
    - Copy the job description you're applying for
    
    **Step 2:** Input job description
    - Paste the complete job description in the text area below
    - Include requirements, skills, and qualifications
    
    **Step 3:** Upload your resume
    - Click "Browse files" and select your PDF resume
    - Wait for "PDF Uploaded Successfully" confirmation
    
    **Step 4:** Choose analysis type
    - **"Tell Me About the Resume"**: Get professional evaluation and feedback
    - **"Percentage Match"**: Get match percentage and missing keywords
    
    **Step 5:** Review results
    - Read the AI-generated analysis carefully
    - Note missing keywords and improvement suggestions
    - Update your resume based on recommendations
    """)

# Applications
with st.expander("🎯 Applications & Use Cases"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Job Seekers:**
        - Resume optimization for specific roles
        - ATS compatibility checking
        - Keyword gap analysis
        - Interview preparation
        """)
    
    with col2:
        st.markdown("""
        **For Recruiters:**
        - Quick resume screening
        - Candidate-role fit assessment
        - Standardized evaluation process
        - Time-efficient hiring
        """)

# Industry Usage
with st.expander("🏢 Industry Applications"):
    st.markdown("""
    **Industries where ATS systems are widely used:**
    
    - **Technology**: Software companies, startups, tech giants
    - **Healthcare**: Hospitals, pharmaceutical companies, medical device firms
    - **Finance**: Banks, investment firms, insurance companies
    - **Consulting**: Management consulting, IT consulting firms
    - **Manufacturing**: Automotive, aerospace, consumer goods
    - **Retail**: E-commerce, fashion, consumer brands
    - **Government**: Federal, state, and local government agencies
    - **Education**: Universities, schools, educational technology companies
    
    **Statistics**: Over 90% of Fortune 500 companies use ATS systems for initial resume screening.
    """)

st.markdown("---")
st.header("🚀 Start Your Resume Analysis")
st.markdown("*Upload your resume and job description to get started with AI-powered analysis*")

input_text=st.text_area("Job Description: ",key="input", height=150, placeholder="Paste the complete job description here...")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")
    st.info(f"File name: {uploaded_file.name}")

st.markdown("### Choose Analysis Type:")
col1, col2 = st.columns(2)

with col1:
    submit1 = st.button("📈 Tell Me About the Resume", use_container_width=True)
    st.caption("Get professional evaluation and detailed feedback")

with col2:
    submit3 = st.button("🎯 Percentage Match", use_container_width=True)
    st.caption("Get match percentage and missing keywords")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None and input_text.strip():
        with st.spinner('🤖 AI is analyzing your resume...'):
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.success("✅ Analysis Complete!")
        st.subheader("📈 Professional Resume Evaluation")
        st.write(response)
        
        # Download Report Button
        pdf_buffer = generate_pdf_report("Professional Resume Evaluation", response, input_text, uploaded_file.name)
        st.download_button(
            label="📄 Download Report as PDF",
            data=pdf_buffer,
            file_name=f"resume_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    elif uploaded_file is None:
        st.error("⚠️ Please upload your resume (PDF format)")
    else:
        st.error("⚠️ Please enter the job description")

elif submit3:
    if uploaded_file is not None and input_text.strip():
        with st.spinner('🎯 Calculating match percentage...'):
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.success("✅ Analysis Complete!")
        st.subheader("🎯 ATS Match Analysis")
        st.write(response)
        
        # Download Report Button
        pdf_buffer = generate_pdf_report("ATS Match Analysis", response, input_text, uploaded_file.name)
        st.download_button(
            label="📄 Download Report as PDF",
            data=pdf_buffer,
            file_name=f"ats_match_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    elif uploaded_file is None:
        st.error("⚠️ Please upload your resume (PDF format)")
    else:
        st.error("⚠️ Please enter the job description")




# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit and Google Gemini Pro Vision AI</p>
    <p>Helping job seekers optimize their resumes for ATS systems</p>
</div>
""", unsafe_allow_html=True)