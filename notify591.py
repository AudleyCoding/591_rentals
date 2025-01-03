import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN") # (replace with your own token)
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify" # Line Notify API URL

# Send Line Notify message
def send_line_message(message):
    """
    Sends a message to the LINE Notify API.
    """
    if not LINE_NOTIFY_TOKEN:
        print("Error: LINE_NOTIFY_TOKEN is not set in the environment.")
        return
    
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
    }
   
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    
def send_links_via_line(links):
    """
    Sends each link as a separate message via LINE Notify.
    After all links, sends a final thumbs-up emoji as confirmation.
    """
    for link in links:
        send_line_message(f"🏠 New rental listing:\n{link}")
    
    # Send final confirmation message
    send_line_message("👍👍👍👍👍👍👍👍")
