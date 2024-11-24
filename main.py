import streamlit as st
from io import BytesIO
from PIL import Image
from util import *

page_title = "QueryVision 🖼️🔍"
page_icon = ":robot_face:"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

if "rag" not in st.session_state:
    st.session_state.rag = None

if "rag_results" not in st.session_state:
    st.session_state.rag_results = None

st.title(page_title)
st.write(':blue[***Answers Visualized from Your Documents 🌟📄***]')
st.write("""
QueryVision 🚀 is your go-to intelligent app for visual insights. Upload any 📂 PDF document, and it seamlessly 
transforms and stores them in a ⚙️ vector database with multimodal embeddings, and 
retrieves the most relevant visuals 🖼️ based on your questions 🤔. Ideal for interactive presentations, detailed 
reports, or creative designs, it ensures your queries get precise, visually enriched answers. 💡✨
""")

# File uploader
st.subheader("Upload a PDF file:", divider='gray')
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed")

# If pdf file is not none then save the contents of the pdf file into temp file and preview the pdf
if uploaded_pdf is not None:
    # Save the contents of the uploaded file into temp file
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_pdf.getvalue())

    process = st.button("Process", type="primary", key="process")
    if process:
        with st.spinner('Creating Document Indexing ...'):
            st.session_state.rag = load_rag_model()
            create_rag_index(st.session_state.rag, temp_file)

    col1, col2 = st.columns([2,1], vertical_alignment="top")

    with col1:
        st.subheader('Chat with PDF:', divider='gray')
        question = st.text_input("Enter your question:", placeholder= 'Enter question related to uploaded document')
        submit = st.button("Submit", type="primary", key="submit", disabled=not question)
        if submit:
            with st.spinner('Searching ...'):
                st.session_state.rag_results = st.session_state.rag.search(question, k=1)


    with (col2):
        st.subheader('PDF Previewer:', divider='gray')
        with st.expander(':blue[***Preview PDF***]', expanded=False):
            display_pdf(uploaded_pdf)
        st.subheader('Reference & Context:', divider='gray')
        if st.session_state.rag_results is not None:
            image_bytes = base64.b64decode(st.session_state.rag_results[0].base64)
            # Open the image using PIL
            image = Image.open(BytesIO(image_bytes))
            with st.expander(':blue[***Referenced Image***]', expanded=True):
                if st.session_state.rag_results[0].score > 8:
                    page_number = st.session_state.rag_results[0].page_num
                    # Display the image
                    st.image(image, caption=f"Referenced Image in page #: {page_number}", use_container_width =True)
                else:
                    st.warning('No Reference Found!')
