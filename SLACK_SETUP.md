# Slack Integration Setup Guide

Complete step-by-step guide to set up Slack notifications for your MCP PR Agent.

## ⚠️ Important Security Notes

- **Never commit webhook URLs to version control**
- **Treat webhook URLs like passwords**
- **Anyone with the URL can post to your Slack channel**
- **Use environment variables, never hardcode**

## Step 1: Create Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. **App Name**: `MCP Course Notifications`
4. **Workspace**: Select your Slack workspace
5. Click **"Create App"**

## Step 2: Enable Incoming Webhooks

1. In your app dashboard, go to **"Features"** → **"Incoming Webhooks"**
2. Toggle **"Activate Incoming Webhooks"** to **ON**
3. Click **"Add New Webhook to Workspace"**

## Step 3: Choose Channel & Authorize

1. **Select Channel**: Choose where notifications will be posted
   - Recommendation: Create a dedicated `#pr-notifications` or `#devops` channel
2. Click **"Authorize"** to allow the app to post

## Step 4: Copy Webhook URL

1. After authorization, you'll see the **"Webhook URL"**
2. **Copy the entire URL** (starts with `https://hooks.slack.com/services/...`)
3. **Save it securely** - you'll need it in the next step

## Step 5: Configure Environment

1. Open your `.env` file:
   ```bash
   # Replace the placeholder with your actual webhook URL
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/ACTUAL/WEBHOOK/URL
   ```

2. **Security Reminder**: Never commit this file with real URLs!

## Step 6: Test Integration

1. Run the test script:
   ```bash
   python test_slack.py
   ```

2. Check your Slack channel for a test message

3. If successful, you'll see:
   ```
   ✅ Success! Message sent to Slack
   🎉 Slack integration is working!
   ```

## Troubleshooting

### ❌ "invalid_payload" error
- Check your webhook URL is correct
- Ensure you're using the full URL
- Verify the app has permission to post to the channel

### ❌ "missing_text" error
- The payload format might be incorrect
- Check the JSON structure in the code

### ❌ "channel_not_found" error
- The app might have been removed from the channel
- Re-add the webhook to the workspace

### ❌ Timeout errors
- Check your internet connection
- Slack API might be temporarily unavailable

## Advanced Configuration

### Multiple Channels
Create separate webhooks for different notification types:
```bash
SLACK_WEBHOOK_CI=https://hooks.slack.com/services/...  # CI/CD notifications
SLACK_WEBHOOK_PR=https://hooks.slack.com/services/...  # PR notifications
```

### Custom Message Formatting
The code supports Slack markdown:
- `*bold text*` for bold
- `_italic text_` for italic
- `code` for inline code
- ```code blocks``` for multi-line code
- `<https://url|Link Text>` for links

## Example Messages

### CI Success
```
✅ *Deployment Successful*

Deployment completed successfully for [Repository Name]

*Changes:*
- Added new user authentication
- Fixed database connection issue

*Links:*
<https://github.com/user/repo|View Changes>
```

### CI Failure
```
🚨 *CI Failure Alert*

A CI workflow has failed:
*Workflow*: Build & Test
*Branch*: main
*Status*: Failed
*View Details*: <https://github.com/user/repo/actions/runs/123|View Logs>

Please check the logs and address any issues.
```

## Security Best Practices

### Environment Variables
- Use `.env` files (never commit)
- Use secure secret management in production
- Rotate webhook URLs periodically

### Permissions
- Use dedicated Slack channels for notifications
- Limit app permissions to only what's needed
- Regularly audit app usage

### Monitoring
- Monitor webhook usage in Slack admin panel
- Set up alerts for unusual activity
- Log notification attempts in your application

## Need Help?

If you encounter issues:

1. Check the [Slack API documentation](https://api.slack.com/messaging/webhooks)
2. Verify your webhook URL format
3. Test with the provided `test_slack.py` script
4. Check application logs for detailed error messages

## Next Steps

Once Slack is configured:
1. Test all notification scenarios
2. Integrate with your CI/CD pipeline
3. Set up monitoring and alerting
4. Document notification policies for your team
