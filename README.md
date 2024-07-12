# AI-agent-PDF-QAbot-with-slack-integration

This Streamlit application allows users to upload a PDF document, input questions, and receive answers generated using OpenAI's language model. The answers are then posted to a Slack channel specified by the user

# Features
Upload PDF: Users can upload a PDF document.
Input Questions: Enter one or multiple questions related to the PDF content.
Submit Button: Trigger the process to generate answers and post them to Slack.
Error Handling: Provides feedback on errors during PDF processing or Slack posting.

# Requirements

Python 3.6+
Install dependencies using pip install -r requirements.txt
Set up environment variables in a .env file
SLACK_TOKEN=your_slack_token
OPENAI_API_KEY=your_openai_api_key
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Usage
1.Clone the repository:

git clone https://github.com/Sreeraga03/AI-agent-PDF-QAbot-with-slack-integration.git

cd repository_name

2.pip install -r requirements.txt

pip install -r requirements.txt

3.Set up environment variables:

Create a .env file in the root directory and add your Slack token, OpenAI API key, and Slack webhook URL.

4.Run the Streamlit app:

streamlit run slack_app.py

5.Use the application:

Upload a PDF file using the file uploader.

Enter one or multiple questions in the text area (one question per line).

Click on the "Submit" button to generate answers and post them to Slack.

# Files 

slack_app.py: Main Streamlit application file.

requirements.txt: List of Python dependencies.

.env: Environment variables file (not included in the repository).
