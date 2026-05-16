import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import base64
from io import BytesIO
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your environment variables or Streamlit secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Page configuration
st.set_page_config(
    page_title="Student Answer Evaluator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
    <h1>📝 Student Answer Evaluator</h1>
    <p>AI-powered evaluation of student handwritten answers</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload Question Paper** - PDF with exam questions
    2. **Upload Answer Sheet** - PDF with student's handwritten answers
    3. **Click Evaluate** - AI will match answers and analyze
    4. **Review Results** - See detailed evaluation with suggestions
    5. **Download Report** - Export results as CSV or JSON
    
    ---
    ### ⚙️ Configuration
    """)
    
    model_choice = st.selectbox(
        "Select AI Model",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        help="Flash: Faster & cheaper | Pro: More accurate & detailed"
    )

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Question Paper")
    question_pdf = st.file_uploader(
        "Choose a PDF file with questions",
        type="pdf",
        key="question_pdf"
    )
    if question_pdf:
        st.success(f"✅ Loaded: {question_pdf.name}")

with col2:
    st.subheader("✍️ Upload Answer Sheet")
    answer_pdf = st.file_uploader(
        "Choose a PDF file with handwritten answers",
        type="pdf",
        key="answer_pdf"
    )
    if answer_pdf:
        st.success(f"✅ Loaded: {answer_pdf.name}")

# Evaluation section
st.divider()

if st.button("🚀 Evaluate Answers", type="primary", use_container_width=True):
    if not question_pdf or not answer_pdf:
        st.error("❌ Please upload both PDFs before evaluating!")
    else:
        with st.spinner("🔄 Processing PDFs..."):
            # Extract text from PDFs
            def extract_text_from_pdf(pdf_file):
                pdf_reader = PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            
            question_text = extract_text_from_pdf(question_pdf)
            answer_text = extract_text_from_pdf(answer_pdf)
            
            if not question_text or not answer_text:
                st.error("❌ Could not extract text from PDFs. Please ensure PDFs contain readable text or images.")
            else:
                st.markdown('<div class="info-box">📊 Starting AI evaluation...</div>', unsafe_allow_html=True)
                
                # Prepare prompt for Gemini
                evaluation_prompt = f"""
You are an expert exam evaluator. Analyze the student's answers against the question paper and provide a detailed evaluation.

QUESTION PAPER:
{question_text}

STUDENT'S ANSWER SHEET:
{answer_text}

Please provide your analysis in the following JSON format:
{{
    "evaluation": [
        {{
            "question_number": 1,
            "question": "The actual question text",
            "student_answer": "What the student wrote",
            "score_percentage": 70,
            "key_points_identified": ["point1", "point2"],
            "missing_key_points": ["point3", "point4"],
            "enhancement_suggestions": ["suggestion1", "suggestion2"],
            "feedback": "Brief feedback on this answer"
        }}
    ],
    "overall_summary": {{
        "total_questions": 10,
        "average_score": 75,
        "strengths": ["strength1", "strength2"],
        "areas_for_improvement": ["area1", "area2"]
    }}
}}

Ensure the JSON is valid and complete. Match each answer to its corresponding question number.
"""
                
                try:
                    # Call Gemini API
                    model = genai.GenerativeModel(model_choice)
                    response = model.generate_content(evaluation_prompt)
                    response_text = response.text
                    
                    # Extract JSON from response
                    try:
                        # Try to find JSON in response
                        start_idx = response_text.find('{')
                        end_idx = response_text.rfind('}') + 1
                        json_str = response_text[start_idx:end_idx]
                        evaluation_data = json.loads(json_str)
                    except (json.JSONDecodeError, ValueError):
                        st.error("❌ Could not parse AI response. Please try again.")
                        st.text(response_text)
                        st.stop()
                    
                    # Display results
                    st.markdown('<div class="success-box">✅ Evaluation Complete!</div>', unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # Overall Summary
                    st.subheader("📊 Overall Summary")
                    summary = evaluation_data.get("overall_summary", {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Questions", summary.get("total_questions", 0))
                    with col2:
                        st.metric("Average Score", f"{summary.get('average_score', 0)}%")
                    with col3:
                        st.metric("Strengths", len(summary.get("strengths", [])))
                    with col4:
                        st.metric("Improvement Areas", len(summary.get("areas_for_improvement", [])))
                    
                    if summary.get("strengths"):
                        st.write("**Strengths:**")
                        for strength in summary.get("strengths", []):
                            st.write(f"✅ {strength}")
                    
                    if summary.get("areas_for_improvement"):
                        st.write("**Areas for Improvement:**")
                        for area in summary.get("areas_for_improvement", []):
                            st.write(f"⚠️ {area}")
                    
                    st.divider()
                    
                    # Detailed Evaluation Table
                    st.subheader("📋 Detailed Evaluation")
                    
                    # Create summary dataframe
                    summary_data = []
                    for item in evaluation_data.get("evaluation", []):
                        summary_data.append({
                            "Q No.": item.get("question_number", ""),
                            "Score %": item.get("score_percentage", 0),
                            "Key Points": ", ".join(item.get("key_points_identified", [])),
                            "Missing Points": ", ".join(item.get("missing_key_points", [])),
                        })
                    
                    if summary_data:
                        df_summary = pd.DataFrame(summary_data)
                        st.dataframe(df_summary, use_container_width=True)
                    
                    st.divider()
                    
                    # Question-wise Details
                    st.subheader("🔍 Question-wise Analysis")
                    
                    for idx, item in enumerate(evaluation_data.get("evaluation", [])):
                        with st.expander(f"Question {item.get('question_number', idx + 1)} (Score: {item.get('score_percentage', 0)}%)"):
                            st.write("**Question:**")
                            st.write(item.get("question", "N/A"))
                            
                            st.write("**Student's Answer:**")
                            st.write(item.get("student_answer", "N/A"))
                            
                            st.write("**Key Points Identified:**")
                            for point in item.get("key_points_identified", []):
                                st.write(f"✅ {point}")
                            
                            st.write("**Missing Key Points:**")
                            for point in item.get("missing_key_points", []):
                                st.write(f"❌ {point}")
                            
                            st.write("**Enhancement Suggestions:**")
                            for suggestion in item.get("enhancement_suggestions", []):
                                st.write(f"💡 {suggestion}")
                            
                            st.write("**Feedback:**")
                            st.info(item.get("feedback", "N/A"))
                    
                    st.divider()
                    
                    # Download Options
                    st.subheader("📥 Download Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # CSV Export
                        if summary_data:
                            csv_data = df_summary.to_csv(index=False)
                            st.download_button(
                                label="📊 Download as CSV",
                                data=csv_data,
                                file_name=f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                    
                    with col2:
                        # JSON Export
                        json_data = json.dumps(evaluation_data, indent=2)
                        st.download_button(
                            label="📄 Download as JSON",
                            data=json_data,
                            file_name=f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"❌ Error during evaluation: {str(e)}")
                    st.write("Please check your API key and try again.")

# Footer
st.divider()
st.markdown("""
---
<center>
    <p>Made with ❤️ using Streamlit & Google Gemini AI</p>
    <p><small>Note: Ensure PDFs are clear and readable for best results</small></p>
</center>
""", unsafe_allow_html=True)
