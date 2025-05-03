from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from youtube_utils import get_transcript
from summarizer import summarize_text

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if "youtube.com" in incoming_msg or "youtu.be" in incoming_msg:
        transcript = get_transcript(incoming_msg)
        if transcript:
            summary = summarize_text(transcript)
            msg.body(summary)
        else:
            msg.body("Couldn't fetch transcript. Try another video link.")
    else:
        msg.body("Please send a valid YouTube link 📺.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
