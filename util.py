import base64
from idlelib.colorizer import prog_group_name_to_tag

import streamlit as st
from byaldi import RAGMultiModalModel
from datetime import datetime


def progress_callback():
    pass
# Function to display the PDF of a given file
def display_pdf(file):
    # Reading the uploaded file
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="600" type="application/pdf"></iframe>'

    # Displaying the PDF
    st.markdown(pdf_display, unsafe_allow_html=True)


def load_rag_model():
    rag = RAGMultiModalModel.from_pretrained('vidore/colpali-v1.2', verbose=10)
    return rag


def create_rag_index(rag, file):
    index_name = datetime.now().strftime("%Y%m%d_%H%M%S_%f") # Create a unique index name based on current date & time
    rag.index(input_path=file, index_name=index_name, store_collection_with_index=True, overwrite=False)
    st.success('Document Index created successfully')