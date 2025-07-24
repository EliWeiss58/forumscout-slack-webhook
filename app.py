from flask import Flask, request
import requests
import threading

app = Flask(__name__)

# Your Slack webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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" def send_to_slack_async(message):
    """Send to Slack in background thread"""
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
    except:
        pass  # Fail silently

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Return immediately, send to Slack in background
    threading.Thread(target=send_to_slack_async, args=("🚀 *ForumScout Webhook Received!*\n\nWorking perfectly!",)).start()
    return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "Fast webhook service running!"

@app.route('/health', methods=['GET'])
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
