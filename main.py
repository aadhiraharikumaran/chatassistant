import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch the GROQ_API_KEY from the environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Check if the API key is loaded correctly
print(f"GROQ_API_KEY: {GROQ_API_KEY}")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-70b-8192'

def get_groq_response(question):
    messages = [
        {
            "role": "system",  # Define the system context for the model
            "content": "You are a very naive, loving boyfriend who loves his girlfriend no matter what. You do not get angry at her no matter what she says and you are very patient. You praise her a lot and are very appreciative of her and you do not wish to lose her. Your role is to give loving responses and diffuse arguments with the girlfriend."
        },
        {
            "role": "user",  # User input
            "content": question,
        }
    ]

    # Send the message to the Groq API
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=4096
        )

        # Print the full response object for debugging
        print("Full Response:", response)

        # Access the 'choices' attribute of the response
        if hasattr(response, 'choices') and len(response.choices) > 0:
            # Access the 'content' of the first choice directly
            choice = response.choices[0]
            if hasattr(choice, 'message'):
                # Directly access the content attribute from the message
                return choice.message.content

        return "Error: Unable to extract the model's response."

    except Exception as e:
        # Capture and log any exceptions
        print(f"Error: {e}")
        return f"There was an issue retrieving a response: {e}"

# Streamlit app title
st.title("How to talk to your girlfriend")

# Input box for user query
query = st.text_input("What did she say?: ")

# Button to get response
if st.button("Search"):
    if query:
        # Get the response from the Groq model
        response = get_groq_response(query)
        # Display the response
        st.write("Response:", response)
    else:
        st.write("Please enter a query.")
