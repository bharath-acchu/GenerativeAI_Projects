from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot_engine import get_chatbot_response
from document_utils import load_and_vectorize
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    print('Incoming msg is:', incoming_msg)

    media_url = request.values.get('MediaUrl0')
    media_type = request.values.get('MediaContentType0')

    response = MessagingResponse()
    msg = response.message()
    print(msg)
    print(msg.body)
    

    # Test print to confirm endpoint hit
    print("Reached whatsapp_reply endpoint")

    # Handle PDF upload
    if media_url and media_type and 'application/pdf' in media_type:
        file_name = f"uploaded_{request.values.get('MessageSid')}.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        twilio_auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        r = requests.get(media_url, auth=twilio_auth)

        if r.status_code == 200 and r.headers['Content-Type'] == 'application/pdf':
            with open(file_path, 'wb') as f:
                f.write(r.content)
            load_and_vectorize(file_path)
            msg.body("✅ PDF uploaded and indexed. Ask your questions.")
        else:
            msg.body("❌ Failed to download the PDF. Please try again.")
    
    # Handle general message
    elif incoming_msg:
        print("Handling general message")
        reply = get_chatbot_response(incoming_msg)
        if not reply or reply.strip() == "":
            reply = "🤖 I'm Gemini PDF ChatBot. Upload a PDF or ask a question."
        msg.body(reply)

    # Fallback
    else:
        msg.body("Please send a message or upload a PDF document.")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
