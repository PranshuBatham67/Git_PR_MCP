# GitHub Repository Integration Guide

Complete guide for integrating the MCP PR Agent with real GitHub repositories for production use.

## Architecture Overview

```
GitHub Repository → Webhooks → Deployed Webhook Server → JSON Storage → MCP Client/LLM → User
```

## Step 1: Deploy the Webhook Server

### Option A: Render (Recommended)

1. **Create Render Account**: Go to [render.com](https://render.com)
2. **Connect Repository**: Link your GitHub repo
3. **Create Web Service**:
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: `8080`

4. **Environment Variables**:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
   HUGGINGFACE_API_TOKEN=your_huggingface_token
   ```

5. **Deploy**: Click "Create Web Service"

6. **Get the URL**: Copy the `.onrender.com` URL for webhooks

### Option B: Railway

```bash
railway login
railway link
railway add --name pr-mcp-webhook
railway up
```

## Step 2: Configure GitHub Webhooks

1. **Go to Repository Settings**:
   - Navigate to your GitHub repo
   - Go to **Settings** → **Webhooks**

2. **Add Webhook**:
   - **Payload URL**: `https://your-deployed-server.onrender.com/webhook/github`
   - **Content type**: `application/json`
   - **Secret**: (leave empty for now)
   - **Events**: Select specific events you want:
     - [x] **Pull requests**
     - [x] **Workflow runs** (for CI/CD)
     - [x] **Push** (optional)

3. **Test Webhook**:
   - Click "Add webhook"
   - GitHub will send a test ping
   - Check your deployed server logs

## Step 3: Set Up Local MCP Client

### For Individual Developers

1. **Clone and Setup**:
   ```bash
   git clone <your-repo>
   cd github-pr-mcp
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Add your tokens
   ```

3. **Run the LLM Client**:
   ```bash
   python llm_client.py
   ```

### Example Queries

```
You: analyze the current PR changes
You: what CI/CD workflows are running
You: suggest a PR template for this bug fix
You: send a team notification about deployment
```

## Step 4: Production Workflow

### For Teams/Organizations

1. **Deploy Webhook Server**: Use Render/Railway for 24/7 availability
2. **Configure Repository Webhooks**: Set up for all active repos
3. **Team Access**: Share the LLM client setup with team members
4. **Monitoring**: Set up alerts for webhook failures

### Real-World Usage Examples

#### Scenario 1: PR Review
```
Developer: "analyze the changes in PR #42"
Assistant: [Calls analyze_file_changes tool]
         [Shows diff, statistics, commits]
         [Suggests appropriate template]
```

#### Scenario 2: CI/CD Monitoring
```
DevOps: "check the status of our CI pipeline"
Assistant: [Calls get_workflow_status tool]
         [Shows current workflow states]
         [Alerts if any are failing]
```

#### Scenario 3: Team Communication
```
PM: "notify the team about the successful deployment"
Assistant: [Calls send_slack_notification tool]
         [Posts formatted message to Slack]
```

## Step 5: Advanced Configuration

### Multiple Repositories

For handling multiple repos, deploy separate webhook servers or use URL routing:

```
repo1.yourdomain.com → handles repo1 webhooks
repo2.yourdomain.com → handles repo2 webhooks
```

### Custom Templates

Add repository-specific templates:
```bash
# Create custom templates in templates/ directory
cp templates/feature.md templates/mobile-feature.md
# Edit with mobile-specific content
```

### CI/CD Integration

Set up automated notifications:
- PR opened → Analyze and suggest template
- CI failed → Alert team in Slack
- Deployment successful → Celebrate in Slack

## Step 6: Monitoring & Maintenance

### Health Checks

Monitor your deployment:
```bash
# Check webhook server health
curl https://your-server.onrender.com/webhook/github

# Check logs in Render/Railway dashboard
```

### Backup & Recovery

- Webhook data is stored as JSON files
- Consider backing up important webhook data
- Monitor disk usage for large repositories

### Security Considerations

- Use HTTPS webhooks only
- Consider adding webhook secrets for verification
- Rotate API tokens regularly
- Limit webhook permissions to read-only where possible

## Troubleshooting

### Webhook Not Receiving Events

1. **Check URL**: Ensure the webhook URL is correct
2. **SSL Required**: GitHub requires HTTPS
3. **Firewall**: Ensure port 8080 is accessible
4. **Logs**: Check deployment logs for connection errors

### LLM Client Issues

1. **Model Loading**: Ensure sufficient RAM (4GB+ recommended)
2. **Dependencies**: Run `pip install -r requirements.txt`
3. **Environment**: Check `.env` file has correct tokens

### Tool Execution Errors

1. **Git Access**: Ensure local git repository exists
2. **File Permissions**: Check read/write permissions for templates
3. **API Limits**: Monitor Hugging Face API usage

## Scaling Considerations

### For Large Teams

- Deploy multiple webhook servers
- Use database instead of JSON files
- Implement rate limiting
- Add authentication/authorization

### For High-Traffic Repos

- Use Redis/queue for webhook processing
- Implement webhook retry logic
- Add monitoring and alerting
- Consider paid LLM APIs for better performance

## Next Steps

1. **Test with Real Repository**: Set up webhooks for an active project
2. **Customize Templates**: Create repo-specific PR templates
3. **Team Training**: Show team members how to use the LLM client
4. **Automate Workflows**: Set up automated PR analysis and notifications
5. **Monitor Usage**: Track which tools are most valuable

Your MCP PR Agent is now ready for production GitHub repository integration! 🚀
