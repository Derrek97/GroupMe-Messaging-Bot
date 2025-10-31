import requests
import json
import sys
import os

# --- Configuration loaded from Environment Variables ---
BOT_ID = os.environ.get("GROUPME_BOT_ID")
API_URL = 'https://api.groupme.com/v3/bots/post'
# -------------------------------------------------------

def send_groupme_message(text):
    """Posts a message to the GroupMe group via the bot."""
    if not BOT_ID:
        print("Error: GROUPME_BOT_ID environment variable not set.")
        sys.exit(1)

    # The JSON payload for the bot message
    data = {
        'bot_id': BOT_ID,
        'text': text
    }
    
    # Send the POST request
    try:
        response = requests.post(API_URL, data=json.dumps(data))
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        print(f"Success! Message sent: '{text[:50]}...'")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_message.py \"Your message text here\"")
        sys.exit(1)
        
    # The message text is passed as the first argument after the script name
    message_to_send = sys.argv[1]
    send_groupme_message(message_to_send)