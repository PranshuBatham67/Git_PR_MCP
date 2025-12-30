
#!/usr/bin/env python3
"""
Test script for Slack webhook integration
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_slack_webhook():
    """Test the Slack webhook URL"""

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not set in .env file")
        return False

    if webhook_url == "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK":
        print("❌ Please replace the placeholder SLACK_WEBHOOK_URL with your actual webhook URL")
        print("   Get it from: https://api.slack.com/apps -> Your App -> Features -> Incoming Webhooks")
        return False

    try:
        # Test message
        payload = {
            "text": "🧪 *Test Message from MCP Course*\n\nYour Slack webhook is working! 🎉\n\n_This is a test from your GitHub PR MCP server._",
            "mrkdwn": True
        }

        print("🚀 Sending test message to Slack...")

        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Success! Message sent to Slack")
            print("   Check your Slack channel for the test message")
            return True
        else:
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your webhook URL")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Slack Webhook Integration")
    print("=" * 40)

    success = test_slack_webhook()

    if success:
        print("\n🎉 Slack integration is working!")
        print("   You can now use the send_slack_notification tool in your MCP server")
    else:
        print("\n🔧 Setup needed:")
        print("   1. Create a Slack app at https://api.slack.com/apps")
        print("   2. Enable Incoming Webhooks")
        print("   3. Add webhook to workspace")
        print("   4. Copy the webhook URL to your .env file")
        print("   5. Run this test again")
