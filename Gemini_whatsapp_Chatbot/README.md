# WhatsApp YouTube Summarizer using Gemini

## Setup Instructions

1. Clone this repository
2. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Create `.env` file and add your Gemini API Key, TWILIO ACCOUNT SID, TWILIO AUTH TOKEN
4. Run Flask app:
    ```bash
    python app.py
    ```

5. Start ngrok:
    ```bash
    ngrok http 5000
    ```

6. Set ngrok HTTPS URL as your Twilio WhatsApp Sandbox Webhook.
7. Upload the pdf document and ask questions related to it

