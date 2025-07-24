from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Slack webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Send a simple message to Slack no matter what
    try:
        slack_message = {
            "text": "🔔 *Webhook Called Successfully!*\n\nForumScout webhook is working!"
        }
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
        return "OK", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/', methods=['GET'])
def home():
    return "Webhook service is running!"

@app.route('/health', methods=['GET'])
def health():
    return "Healthy!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
