import streamlit as st
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from pathlib import Path
from PyPDF2 import PdfReader
import openai

# Load environment variables from the .env file
load_dotenv(Path('.') / '.env')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Fetch the Slack token, OpenAI API key, and Slack webhook URL from environment variables
slack_token = os.getenv("SLACK_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

if not slack_token:
    raise ValueError("SLACK_TOKEN is not set in the environment variables.")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Initialize Slack WebClient
client = WebClient(token=slack_token)

# Set OpenAI API key
openai.api_key = openai_api_key

# Function to read PDF content
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        raise

# Function to generate answers using OpenAI
def generate_answers(pdf_text, questions):
    answers = {}
    for question in questions:
        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-0125",
                prompt=f"Answer the following question based on the provided text:\n\nText: {pdf_text}\n\nQuestion: {question}",
                max_tokens=150
            )
            answer = response.choices[0].text.strip() if response.choices else "Data Not Available"
            answers[question] = answer
        except Exception as e:
            logging.error(f"Error generating answer for question '{question}': {e}")
            answers[question] = "Data Not Available"
    return answers

# Function to post formatted answers to Slack
def post_to_slack(channel_name, message):
    try:
        # Get the list of channels and find the channel ID for the specified channel_name
        channel_id = None
        channels_response = client.conversations_list()
        for channel in channels_response['channels']:
            if channel['name'] == channel_name:
                channel_id = channel['id']
                break
        
        if not channel_id:
            raise ValueError(f"Channel '{channel_name}' not found.")
        
        # Post a message to the channel
        response = client.chat_postMessage(channel=channel_id, text=message)
        logging.debug(response)
    except SlackApiError as e:
        logging.error(f"Error posting message to Slack: {e.response['error']}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Streamlit app function
def streamlit_app():
    st.title("PDF Q&A Chatbot")
    
    # File upload for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    # Input questions
    st.subheader("Enter your questions (one per line):")
    questions_input = st.text_area("Questions", height=150)
    
    # Submit button
    if st.button("Submit"):
        if uploaded_file is not None and questions_input.strip():
            try:
                # Save the uploaded PDF temporarily
                with open("uploaded_pdf.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process the PDF and questions
                pdf_path = "uploaded_pdf.pdf"
                questions = [q.strip() for q in questions_input.split("\n") if q.strip()]
                channel_name = "aiagent"  # Slack channel name
                pdf_text = read_pdf(pdf_path)
                answers = generate_answers(pdf_text, questions)
                
                # Format answers for Slack
                formatted_answers = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])
                
                # Post formatted answers to Slack
                post_to_slack(channel_name, formatted_answers)
                
                st.success("Answers posted to Slack!")
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    streamlit_app()
