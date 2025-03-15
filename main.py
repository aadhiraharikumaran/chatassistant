import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch the GROQ_API_KEY from the environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-70b-8192'

# Function to get response from the Groq model
def get_groq_response(question):
    messages = [
        {
            "role": "angry girlfriend",
            "content": "You are a very naive, loving boyfriend who loves his girlfriend no matter what. You do not get angry at her no matter what she says and you are very patient. You praise her a lot and are very appreciative of her and you do not wish to lose her. Your role is to give loving responses and diffuse arguments with the girlfriend"
        },
        {
            "role": "user",
            "content": question,
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096
    )
    
    return response.choices[0].message.content

# Add custom CSS for the app's appearance
st.markdown("""
    <style>
    body {
        background-color: #FFA9CB;  /* Background color */
        color: #F2799B;  /* Text color */
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #ED408B;  /* Heading color */
    }
    .stButton>button {
        background-color: #ED408B;  /* Button background color */
        color: white;
        padding: 12px 25px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #F2799B;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 12px;
        border: 2px solid #ED408B;
        color: #F2799B;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ED408B;
    }
    .chat-bubble-user {
        background-color: #F2799B;
        color: white;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 15px;
        width: fit-content;
        max-width: 75%;
        align-self: flex-start;
    }
    .chat-bubble-assistant {
        background-color: #ED408B;
        color: white;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 15px;
        width: fit-content;
        max-width: 75%;
        align-self: flex-end;
    }
    .stMarkdown {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered")
st.title("💬 How to Talk to Your Girlfriend")

# Input box for user query
with st.form(key='query_form'):
    query = st.text_input("What did Madhuma say?:", key='user_input')
    submit_button = st.form_submit_button("Send")

# Displaying the chat bubbles
if 'messages' not in st.session_state:
    st.session_state.messages = []

if submit_button and query:
    response = get_groq_response(query)
    
    # Add user's message
    st.session_state.messages.append({"role": "user", "content": query})
    # Add assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
# Display all the messages in the chat interface
if len(st.session_state.messages) > 0:
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-bubble-user"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-assistant"><b>Assistant:</b> {message["content"]}</div>', unsafe_allow_html=True)

# Display styled heading and prompt for user
st.markdown('### **What did Madhuma say?**')
st.markdown("This is how you must respond to diffuse arguments and make her feel loved again! 💡")

