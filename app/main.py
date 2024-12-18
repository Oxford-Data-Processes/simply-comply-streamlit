import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
from aws_utils import iam

# Page configuration
st.set_page_config(
    page_title="Interlife | Document Management",
    page_icon="📑",
    layout="wide",
)

# Custom CSS for professional styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        /* Global font override */
        * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Main content styling */
        .main {
            padding: 2rem;
        }
        
        /* Override ALL Streamlit elements */
        .stMarkdown, .stText, p, span, label, .stTextInput > label, 
        .stSelectbox > label, .stFileUploader > label {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Header styling */
        h1, h2, h3, .stTitle, div.stTitle > h1 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #1a1a1a !important;
            letter-spacing: -0.5px !important;
        }
        
        .stTitle > h1 {
            font-size: 2.5rem !important;
            margin-bottom: 2rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #0066FF !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            font-size: 1rem !important;
            letter-spacing: 0.3px !important;
        }
        
        .stButton > button:hover {
            background-color: #0052CC !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(-1px) !important;
        }
        
        /* File uploader styling */
        .uploadedFile {
            background-color: #F8F9FA !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: #E6F4EA !important;
            color: #1E4620 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Error message styling */
        .stError {
            background-color: #FDE7E9 !important;
            color: #B71C1C !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* File uploader specific styles */
        .stFileUploader > div {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        .stFileUploader > div > div {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Spinner text */
        .stSpinner > div {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Help text */
        .stFileUploader [data-baseweb="help-text"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.9rem !important;
            color: #666 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Main content
st.title("Document Management Portal")
st.markdown(
    """
    <div style='margin-bottom: 2rem;'>
        <p style='font-size: 1.1rem; color: #666; margin-bottom: 2rem; font-family: "Plus Jakarta Sans", sans-serif;'>
            Securely upload and manage your documents with enterprise-grade security and compliance.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# Initialize AWS
iam.get_aws_credentials(st.secrets["aws_credentials"])
s3_client = boto3.client("s3")

# File upload section
st.markdown("### Document Upload")
st.markdown(
    """
    <p style='color: #666; margin-bottom: 1rem; font-family: "Plus Jakarta Sans", sans-serif;'>
        Upload PDF documents for secure storage and processing. All files are encrypted at rest.
    </p>
""",
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "Drag and drop PDF files here",
    type=["pdf"],
    accept_multiple_files=True,
    help="Supported format: PDF. Maximum file size: 200MB",
)

if uploaded_files:
    st.markdown("### Selected Documents")
    for file in uploaded_files:
        st.markdown(
            f"""
            <div style='background-color: #F8F9FA; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; font-family: "Plus Jakarta Sans", sans-serif;'>
                📄 {file.name} ({round(file.size/1024/1024, 2)} MB)
            </div>
        """,
            unsafe_allow_html=True,
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Upload Documents", use_container_width=True):
            with st.spinner("Processing your documents..."):
                for uploaded_file in uploaded_files:
                    try:
                        s3_client.upload_fileobj(
                            uploaded_file,
                            "simply-comply-bucket-654654324108",
                            f"documents_raw/{uploaded_file.name}",
                        )
                    except NoCredentialsError:
                        st.error(
                            "⚠️ Authentication Error: Please check your credentials."
                        )
                    except Exception as e:
                        st.error(f"⚠️ Upload Error: {str(e)}")
                st.success("✅ All documents uploaded successfully!")
                st.balloons()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem; font-family: "Plus Jakarta Sans", sans-serif;'>
        <p>Interlife © 2024 | Enterprise Document Management Solution</p>
        <p style='font-size: 0.8rem;'>SOC 2 Type II Certified | HIPAA Compliant | GDPR Ready</p>
    </div>
""",
    unsafe_allow_html=True,
)
