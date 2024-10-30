import streamlit as st
import PyPDF2

# CSS to customize the file uploader
st.markdown(
    """
    <style>
    .stFileUploader {
        min-height: 200px;  /* Increase the height */
        border: 2px dashed #808080;  /* Style the border */
        border-radius: 10px;  /* Rounded corners */
        padding: 20px;  /* Padding inside the uploader */
        text-align: center;  /* Center the text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to read text files
def read_text_file(file):
    return file.read().decode("utf-8")

# Function to read PDF files
def read_pdf_file(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Main app
st.title("Document Loader")

# File uploader
uploaded_file = st.file_uploader("Upload a Document", type=["txt", "pdf"], label_visibility="collapsed")

# Process the uploaded file
if uploaded_file is not None:
    file_type = uploaded_file.type

    # Handle text files
    if file_type == "text/plain":
        st.subheader("Text File Content:")
        content = read_text_file(uploaded_file)
        st.text_area("Content", content, height=300)

    # Handle PDF files
    elif file_type == "application/pdf":
        st.subheader("PDF File Content:")
        content = read_pdf_file(uploaded_file)
        st.text_area("Content", content, height=300)

    else:
        st.error("Unsupported file type. Please upload a .txt or .pdf file.")