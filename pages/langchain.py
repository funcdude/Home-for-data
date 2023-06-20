import streamlit as st

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter



st.title('🦜🔗 Langchain, OpenAI chat demo')

st.text('This app uses the OPEN AI API, GPT 3.5 version, no conversational memory') 


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

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are 3 key advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)