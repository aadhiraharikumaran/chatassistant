import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import logging
import groq  # Added to handle groq exceptions

# Set Streamlit page configuration (this must be at the top of the script)
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered")

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from the .env file
load_dotenv()

# Fetch the GROQ_API_KEY from the environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-70b-8192'

# Function to get response from the Groq model with error handling
def get_groq_response(question):
    # Standardize the roles to 'system', 'user', 'assistant'
    messages = [
        {
            "role": "system",  # You can use 'system' to set up context for the assistant
            "content": "You are a very naive, loving boyfriend who loves his girlfriend no matter what. You do not get angry at her no matter what she says and you are very patient. You praise her a lot and are very appreciative of her and you do not wish to lose her. Your role is to give loving responses and diffuse arguments with the girlfriend."
        },
        {
            "role": "user",  # Standard role for the user
            "content": question,
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=4096
        )
        logging.debug(response)  # Log the full response for debugging
        return response.choices[0].message.content
    except groq.BadRequestError as e:
        logging.error(f"BadRequestError: {e}")
        st.error(f"BadRequestError: {e}")
        return "There was an error with the API request. Please check the format or your API key."
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        st.error(f"An unexpected error occurred: {e}")
        return "Something went wrong. Please try again later."

# Add custom CSS
st.markdown("""
    <style>
    body {
        background-color: #FFA9CB;
        color: #F2799B;
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #ED408B;
    }
    .stButton>button {
        background-color: #ED408B;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #ED408B;
        color: #F2799B;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ED408B;
    }
    .chat-bubble-user {
        background-color: #F2799B;
        color: white;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 15px;
        width: fit-content;
        max-width: 75%;
        align-self: flex-start;
    }
    .chat-bubble-assistant {
        background-color: #ED408B;
        color: white;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 15px;
        width: fit-content;
        max-width: 75%;
        align-self: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title
st.title("💬 How to Talk to Madhuma")

# Input box for user query
with st.form(key='query_form'):
    query = st.text_input("What did Madhuma say? :", key='user_input')
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
    
if len(st.session_state.messages) > 0:
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-bubble-user"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-assistant"><b>Assistant:</b> {message["content"]}</div>', unsafe_allow_html=True)

# Display styled heading and prompt for user
st.markdown('### **This is how you diffuse arguments and make her feel loved again**')
st.markdown("Made to develop a healthy relationship by Madhuma <3")
