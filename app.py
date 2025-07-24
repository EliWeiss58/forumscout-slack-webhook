from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Your Slack webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

@app.route('/webhook', methods=['POST'])
def transform_webhook():
    try:
        # Get the JSON data from ForumScout
        forumscout_data = request.get_json()
        
        # Handle test events
        if forumscout_data.get('event') == 'test':
            slack_message = {
                "text": "✅ *ForumScout Webhook Test Successful!*\n\nYour webhook integration is working correctly."
            }
        else:
            # Transform the data for regular mentions
            mentions = forumscout_data.get('mentions', [])
            scout_info = forumscout_data.get('scout', {})
            
            if not mentions:
                slack_message = {
                    "text": "📭 No new mentions found in this ForumScout update."
                }
            else:
                # Format multiple mentions
                message_parts = []
                message_parts.append(f"🔍 *New ForumScout Alert - {len(mentions)} mention(s) found*")
                message_parts.append(f"*Query:* {scout_info.get('query', 'Unknown')}")
                message_parts.append("")  # Empty line
                
                for i, mention in enumerate(mentions, 1):
                    # Get sentiment emoji
                    sentiment = mention.get('sentiment', 'Neutral')
                    sentiment_emoji = {
                        'Positive': '😊',
                        'Negative': '😞',
                        'Neutral': '😐'
                    }.get(sentiment, '😐')
                    
                    # Format each mention
                    message_parts.append(f"*Mention #{i}:*")
                    message_parts.append(f"📰 *Title:* {mention.get('title', 'No title')}")
                    message_parts.append(f"🌐 *Source:* {mention.get('source', 'Unknown')} ({mention.get('domain', 'N/A')})")
                    message_parts.append(f"👤 *Author:* {mention.get('author', 'Unknown')}")
                    message_parts.append(f"{sentiment_emoji} *Sentiment:* {sentiment}")
                    message_parts.append(f"🎯 *Match Score:* {mention.get('match_score', 'N/A')}")
                    
                    # Format snippet (truncate if too long)
                    snippet = mention.get('snippet', '')
                    if len(snippet) > 200:
                        snippet = snippet[:200] + "..."
                    message_parts.append(f"💬 *Snippet:* {snippet}")
                    
                    # Add URL
                    url = mention.get('url', '')
                    if url:
                        message_parts.append(f"🔗 *Link:* {url}")
                    
                    message_parts.append("")  # Empty line between mentions
                
                slack_message = {
                    "text": "\n".join(message_parts)
                }
        
        # Send to Slack
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
        
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Sent to Slack"}), 200
        else:
            return jsonify({"status": "error", "message": f"Slack returned {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "ForumScout to Slack transformer is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
