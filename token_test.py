import os
import requests

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
API_URL = "https://notify-api.line.me/api/notify"

def send_line_notification(message):
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
    }
    payload = {
        "message": message,
    }

    response = requests.post(API_URL, headers=headers, data=payload)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")

# Example usage
send_line_notification("Hello, this is a test message to the group!")

