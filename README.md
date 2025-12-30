# GitHub PR MCP Server with Cloud Integration

A Model Context Protocol (MCP) server for analyzing GitHub pull requests, providing AI-powered summaries and template suggestions using Hugging Face.

## Features

- 🔍 **Git Analysis**: Analyze file changes and commit history
- 📝 **PR Templates**: 7 professional PR templates (Bug Fix, Feature, Docs, etc.)
- 🤖 **AI Integration**: Hugging Face powered PR summarization and description generation
- 🔄 **GitHub Actions**: Webhook integration for CI/CD status monitoring
- 💬 **Slack Notifications**: Automated team notifications
- 🐳 **Container Ready**: Docker deployment support

## Architecture

- `server.py`: Main MCP server with analysis tools
- `webhook_server.py`: GitHub webhook receiver
- `templates/`: PR template files
- Cloud integration via Hugging Face Inference API

## Quick Start

### Local Development

1. **Clone and setup:**
   ```bash
   git clone <your-repo>
   cd github-pr-mcp
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

3. **Test integrations:**
   ```bash
   python test_slack.py  # Test Slack webhook
   ```

4. **Run LLM Client (recommended):**
   ```bash
   python llm_client.py
   ```

5. **Or run MCP server directly:**
   ```bash
   python server.py
   ```

6. **Run webhook server (separate terminal):**
   ```bash
   python webhook_server.py
   ```

### Docker Deployment

1. **Build and run:**
   ```bash
   docker-compose up -d
   ```

2. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

### Cloud Deployment Options

#### Railway
```bash
# Deploy webhook server
railway login
railway link
railway add --name pr-mcp-webhook
railway up
```

#### Render
1. Connect GitHub repo to Render
2. Set environment variables in dashboard
3. Deploy as web service

#### Hugging Face Spaces
For the AI components, deploy as a Space with Gradio interface.

## Environment Variables

```bash
# Required
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
HUGGINGFACE_API_TOKEN=your_huggingface_token

# Optional
GITHUB_TOKEN=your_github_token  # For enhanced Git operations
```

### Slack Setup
See [SLACK_SETUP.md](SLACK_SETUP.md) for complete Slack webhook configuration guide.

## Available Tools

### Core Analysis
- `analyze_file_changes`: Git diff analysis
- `get_pr_templates`: List available templates
- `suggest_template`: AI template recommendations

### Cloud AI
- `summarize_pr_changes`: Hugging Face powered summarization
- `generate_pr_description`: AI PR description generation

### CI/CD Integration
- `get_recent_actions_events`: GitHub Actions events
- `get_workflow_status`: Workflow monitoring
- `send_slack_notification`: Team notifications

## How End Users Interact

### Production Deployment Flow

1. **Repository Owners** set up GitHub webhooks pointing to your deployed server
2. **Webhook Server** receives GitHub events (PRs, CI/CD runs) and stores them
3. **Developers** use the LLM client locally to analyze PRs and get AI assistance

### User Interaction Methods

#### Method 1: LLM Client (Recommended)
```bash
python llm_client.py
```
**Natural language queries:**
```
You: analyze the changes in my current branch
You: suggest a PR template for this feature
You: check CI/CD status
You: send deployment notification to Slack
```

#### Method 2: Direct MCP Server
```bash
python server.py  # Runs MCP server for MCP-compatible clients
```

#### Method 3: Webhook-Only
- Automated processing of GitHub events
- Data stored for later analysis
- No direct user interaction

### Real-World Integration Examples

#### Scenario: Developer Working on PR
```
1. Developer pushes code to feature branch
2. GitHub sends webhook to deployed server
3. Server stores PR data
4. Developer runs: python llm_client.py
5. Asks: "analyze my current PR changes"
6. LLM client fetches data and provides analysis
```

#### Scenario: Team CI/CD Monitoring
```
1. CI pipeline runs on GitHub Actions
2. Webhook server receives workflow events
3. Team member asks: "check our CI status"
4. Gets real-time workflow status
5. Can send Slack alerts if needed
```

## API Usage

The webhook server accepts GitHub webhooks at:
```
POST https://your-deployed-server.onrender.com/webhook/github
```

See [GITHUB_INTEGRATION.md](GITHUB_INTEGRATION.md) for complete GitHub setup guide.

## Testing

```bash
pytest test_server.py -v
```

## Deployment Checklist

- [ ] Set environment variables
- [ ] Configure GitHub webhooks
- [ ] Test local deployment
- [ ] Deploy to cloud platform
- [ ] Verify webhook connectivity
- [ ] Test AI integration
- [ ] Monitor logs and performance

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## License

MIT License
