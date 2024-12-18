import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
from aws_utils import iam

iam.get_aws_credentials(st.secrets["aws_credentials"])
# Initialize S3 client
s3_client = boto3.client("s3")

# Streamlit app title
st.title("Interlife File Uploader")

# File uploader widget allowing multiple file uploads, only PDFs
uploaded_files = st.file_uploader(
    "Choose PDF files", type=["pdf"], accept_multiple_files=True
)

# Upload button
if uploaded_files:
    if st.button("Upload Files"):
        for uploaded_file in uploaded_files:
            try:
                # Upload the file to S3
                s3_client.upload_fileobj(
                    uploaded_file,
                    "simply-comply-bucket-654654324108",
                    f"documents_raw/{uploaded_file.name}",
                )

            except NoCredentialsError:
                st.error("Credentials not available.")
            except Exception as e:
                st.error(f"An error occurred while uploading the file: {e}")
        st.success("All files uploaded successfully!")
