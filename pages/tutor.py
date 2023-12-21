import streamlit as st
import langchain
import os
from openai import OpenAI
import time

# load_dotenv()  # take environment variables from .env

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

QUIZ_TUTOR_ID = "asst_Qjw6vQ6WRuIwyyfMtTPYIZJo"

st.title(' Quizzes based on an uploaded PDF document')

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
    "Quiz yourself about the file you uploaded",
    placeholder="Can you create a quiz for me?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not openai_api_key:
    st.info("Please add your OPEN AI API key to continue.")

   
#So that we can see the JSON outputs from the model
import json

def show_json(obj):
    display(json.loads(obj.model_dump_json()))

# using the OpenAI librarires, we create two functions 

client = OpenAI()

# functions to submit a message, containing assistant_id, thread_id - and get a response in the thread
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
thread = client.beta.threads.create()


#function that creates a thread and runs them with the message to the target assistant

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(QUIZ_TUTOR_ID, thread, user_input)
    return thread, run

# Emulating concurrent user requests
thread1, run1 = create_thread_and_run(
    ""
)

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run
# Wait for Run 1
run1 = wait_on_run(run1, thread1)
response_data = pretty_print(get_response(thread1))

# Display the response_data as JSON
st.write(response_data)

# Wait for Run 2
#run2 = wait_on_run(run2, thread2)
#pretty_print(get_response(thread2))

