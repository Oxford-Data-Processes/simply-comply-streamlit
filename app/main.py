import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
from aws_utils import iam

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
                iam.get_aws_credentials(st.secrets["aws_credentials"])
                s3_client = boto3.client("s3")
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


# Move footer to the bottom of the page
st.markdown(
    "<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True
)  # Add space before the footer
st.markdown(
    """
    <footer style='text-align: center; padding: 20px;'>
        <p style='margin: 0;'>GDPR Compliant</p>
        <p style='margin: 0;'>© 2024 INTERLIFE. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
