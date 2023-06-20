import streamlit as st
import langchain
import os

from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain

st.title(' Question and Answers based on an uploaded PDF document')

with st.sidebar:
  openai_api_key = st.text_input('OpenAI API Key')

  # Try to check if API key is empty

  try:
    if not openai_api_key:
        raise ValueError("The API key is empty")
    
    # You can now use openai_api_key for further actions
    
  except ValueError as e:
    # Displaying a message to the user to input the API key
    st.warning(str(e))

    # If API key is provided via input, set it as environment variable
if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

question = st.text_input(
    "Ask something about the file you uploaded",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not openai_api_key:
    st.info("Please add your OPEN AI API key to continue.")

if uploaded_file and question and openai_api_key:
   
   doc_reader = PdfReader(uploaded_file)


    # read data from the file and put them into a variable called raw_text
   raw_text = ''
   for i, page in enumerate(doc_reader.pages):
       text = page.extract_text()
       if text:
           raw_text += text
    # st.info(len(raw_text))

    # Splitting up the text into smaller chunks for indexing
   text_splitter = CharacterTextSplitter(        
       separator = "\n",
       chunk_size = 1000,
       chunk_overlap  = 200, #striding over the text
       length_function = len,
   )
   pages = text_splitter.split_text(raw_text)

   # st.info(pages[1])

   # Download embeddings from OpenAI, setting up FAISS for similarity search

   embeddings = OpenAIEmbeddings()

   docsearch = FAISS.from_texts(pages, embeddings)

   chain = load_qa_chain(OpenAI(), chain_type="stuff") # we are going to stuff all the docs in at once
   docs = docsearch.similarity_search(question,k=10) # the k-value tells how many similar values to return
   results = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
                   
   chain.run(input_documents=docs, question=question)
   
   st.write(results)

  

