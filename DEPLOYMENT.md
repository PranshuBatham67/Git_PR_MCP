# Deployment Guide

## ✅ What Was Fixed

### 1. **Docker Port Binding Issue**
**Problem**: The application was binding to `localhost` instead of `0.0.0.0`, making it inaccessible from outside the container.

**Solution**: 
- Added explicit `ENV HOST=0.0.0.0` and `ENV PORT=8080` in Dockerfile
- Updated `render.yaml` to include these environment variables
- Improved Dockerfile structure for better security and caching

### 2. **Health Check Endpoint**
**Problem**: Render couldn't verify the service was running.

**Solution**: 
- Added `GET /` endpoint that returns `{"status": "healthy"}`
- This matches the health check configuration in `render.yaml`

### 3. **Dockerfile Improvements**
**Problem**: User creation happened after file operations, causing permission issues.

**Solution**: 
- Reorganized Dockerfile to create non-root user first
- Set proper ownership early
- Combined RUN commands for better layer caching
- Followed Docker best practices

---

## 🚀 Deployment Steps

### 1. **Commit and Push Changes**

```bash
git add Dockerfile render.yaml webhook_server.py
git commit -m "fix: Configure proper port binding for Render deployment"
git push origin main
```

### 2. **Deploy on Render**

Render will automatically detect the push and redeploy. You should see:

```
✅ Building Docker image...
✅ Installing dependencies...
✅ Starting webhook server on http://0.0.0.0:8080
✅ Health check passed
✅ Deploy successfully completed
```

### 3. **Verify Deployment**

Once deployed, test the health check:

```bash
curl https://your-render-url.onrender.com/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "GitHub PR MCP Webhook Server"
}
```

---

## 🔧 Environment Variables to Set in Render

In your Render dashboard, set these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `HOST` | `0.0.0.0` | ✅ Yes |
| `PORT` | `8080` | ✅ Yes |
| `SLACK_WEBHOOK_URL` | Your Slack webhook URL | ⚠️ If using Slack |
| `HUGGINGFACE_API_TOKEN` | Your HuggingFace token | ⚠️ If using AI features |

> **Note**: `HOST` and `PORT` are already set via Dockerfile ENV, but can be overridden in Render dashboard if needed.

---

## 📡 Webhook Configuration

### GitHub Webhook Setup

1. Go to your GitHub repository settings
2. Navigate to **Webhooks** → **Add webhook**
3. Set:
   - **Payload URL**: `https://your-render-url.onrender.com/webhook/github`
   - **Content type**: `application/json`
   - **Events**: Select events you want to monitor (e.g., Pull Requests, Workflow runs, Check runs)
4. Click **Add webhook**

### Test the Webhook

Create a test PR or trigger a workflow to verify:

```bash
# View recent events (if you have access to the server)
cat github_events.json
```

---

## 🐛 Troubleshooting

### Issue: "No open ports detected on 0.0.0.0"

**Cause**: Application binding to localhost instead of 0.0.0.0

**Solution**: 
- Ensure `HOST=0.0.0.0` is set in environment variables
- Rebuild the Docker image to pick up new Dockerfile changes

### Issue: "Health check timeout"

**Cause**: Health check endpoint not responding

**Solution**:
- Verify the application starts correctly: Check Render logs
- Test locally: `docker build -t test . && docker run -p 8080:8080 test`
- Visit `http://localhost:8080/` - should return `{"status": "healthy"}`

### Issue: "Container exits immediately"

**Cause**: Python dependencies or code errors

**Solution**:
- Check Render build logs for errors
- Verify `requirements.txt` is complete
- Test locally with Docker

---

## 🧪 Local Testing

### Test with Docker (Recommended)

```bash
# Build the image
docker build -t mcp-pr-webhook .

# Run the container
docker run -p 8080:8080 \
  -e HOST=0.0.0.0 \
  -e PORT=8080 \
  mcp-pr-webhook

# In another terminal, test the endpoints
curl http://localhost:8080/
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -d '{"action": "opened", "repository": {"full_name": "test/repo"}}'
```

### Test Directly with Python

```bash
# Install dependencies
pip install -r requirements.txt

# Export environment variables
export HOST=0.0.0.0
export PORT=8080

# Run the server
python webhook_server.py
```

---

## 📊 Monitoring

### Check Service Status

```bash
# Health check
curl https://your-render-url.onrender.com/

# Check Render logs
# Go to Render dashboard → Your service → Logs
```

### View Events

The webhook server stores the last 100 events in `github_events.json`. This file can be read by the MCP server running locally.

---

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit sensitive tokens to git
2. **Webhook Secret**: Consider adding GitHub webhook secret verification
3. **Rate Limiting**: Add rate limiting for production use
4. **HTTPS Only**: Render provides HTTPS by default - use it
5. **Non-root User**: ✅ Already configured in Dockerfile

---

## 📝 Next Steps

1. ✅ Push the changes to trigger deployment
2. ✅ Verify health check endpoint works
3. ✅ Configure GitHub webhook
4. ✅ Test with a real PR or workflow event
5. ✅ Monitor logs for any issues
6. ⚠️ (Optional) Add webhook secret validation for security
7. ⚠️ (Optional) Set up monitoring/alerting

---

## 🎯 Key Changes Summary

### `Dockerfile`
- ✅ Set `ENV HOST=0.0.0.0` and `ENV PORT=8080`
- ✅ Improved user creation and permissions
- ✅ Better layer caching

### `webhook_server.py`
- ✅ Added GET `/` health check endpoint
- ✅ Already had proper host binding from environment

### `render.yaml`
- ✅ Added explicit HOST and PORT environment variables
- ✅ Health check path set to `/`

---

## 💡 Why This Works

**Before**: Application was listening on `127.0.0.1:8080` (localhost only)
- Render couldn't connect because localhost is internal to the container
- Port scanning failed

**After**: Application listens on `0.0.0.0:8080` (all network interfaces)
- Render can connect from outside the container
- Health checks pass
- Deployment succeeds! 🎉
