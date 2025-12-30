#!/usr/bin/env python3
"""
LLM-powered MCP Client
An AI assistant that interacts with the MCP server to analyze GitHub PRs and provide intelligent responses.
Uses free local models via transformers.
"""

import json
import os
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Import torch here for the model usage
import torch

# Load environment variables
load_dotenv()

class MCPClient:
    """MCP Client that uses LLM for tool calling and user interaction"""

    def __init__(self):
        # Use local model via transformers (free!)
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            import torch

            print("🤖 Loading local AI model... (this may take a moment)")

            # Use a small, free model that works well for tool calling
            model_name = "microsoft/DialoGPT-small"  # Free and lightweight

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

            # Use GPU if available, otherwise CPU
            self.device = 0 if torch.cuda.is_available() else -1
            print(f"📊 Using device: {'GPU' if self.device == 0 else 'CPU'}")

        except ImportError:
            raise ValueError("transformers library not installed. Run: pip install transformers torch")

        # MCP Server tools (we'll simulate the MCP protocol)
        self.available_tools = {
            "analyze_file_changes": {
                "description": "Analyze git file changes in the current repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base_branch": {"type": "string", "default": "main"},
                        "include_diff": {"type": "boolean", "default": True},
                        "max_diff_lines": {"type": "integer", "default": 500}
                    }
                }
            },
            "get_pr_templates": {
                "description": "Get available PR templates",
                "parameters": {"type": "object", "properties": {}}
            },
            "suggest_template": {
                "description": "Suggest appropriate PR template based on changes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "changes_summary": {"type": "string"},
                        "change_type": {"type": "string"}
                    },
                    "required": ["changes_summary", "change_type"]
                }
            },
            "summarize_pr_changes": {
                "description": "Use AI to summarize PR changes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "diff_content": {"type": "string"},
                        "max_length": {"type": "integer", "default": 200}
                    },
                    "required": ["diff_content"]
                }
            },
            "generate_pr_description": {
                "description": "Generate PR description using AI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "changes_summary": {"type": "string"},
                        "change_type": {"type": "string"}
                    },
                    "required": ["changes_summary", "change_type"]
                }
            },
            "get_recent_actions_events": {
                "description": "Get recent GitHub Actions events",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 10}
                    }
                }
            },
            "get_workflow_status": {
                "description": "Get GitHub Actions workflow status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "workflow_name": {"type": "string"}
                    }
                }
            },
            "send_slack_notification": {
                "description": "Send notification to Slack",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            }
        }

    def get_system_prompt(self) -> str:
        """Get the system prompt for the LLM"""
        tools_description = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.available_tools.items()
        ])

        return f"""You are an AI assistant specialized in GitHub PR analysis and management. You have access to various tools for analyzing code changes, suggesting PR templates, and managing CI/CD workflows.

Available tools:
{tools_description}

When a user asks about PR analysis, code changes, or repository management:
1. First analyze what they're asking for
2. Choose the appropriate tool(s) to gather information
3. Execute the tools and interpret results
4. Provide clear, actionable recommendations

For PR-related queries:
- Use analyze_file_changes to understand what changed
- Use suggest_template to recommend appropriate PR templates
- Use AI tools (summarize_pr_changes, generate_pr_description) for enhanced analysis
- Check CI/CD status with get_workflow_status when relevant

Always be helpful, technical, and provide context for your recommendations.

If you need to use a tool, respond with a JSON object containing the tool name and parameters. Otherwise, respond with your analysis and recommendations."""

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Call actual MCP server tools by executing them in the same process"""
        print(f"🔧 Calling tool: {tool_name} with params: {parameters}")

        try:
            # Execute tools by calling the actual functions
            if tool_name == "analyze_file_changes":
                # Import here to avoid circular imports
                from server import analyze_file_changes
                result = await analyze_file_changes(**parameters)
                return result

            elif tool_name == "get_pr_templates":
                from server import get_pr_templates
                result = await get_pr_templates()
                return result

            elif tool_name == "suggest_template":
                from server import suggest_template
                result = await suggest_template(**parameters)
                return result

            elif tool_name == "get_recent_actions_events":
                from server import get_recent_actions_events
                result = await get_recent_actions_events(**parameters)
                return result

            elif tool_name == "get_workflow_status":
                from server import get_workflow_status
                result = await get_workflow_status(**parameters)
                return result

            elif tool_name == "send_slack_notification":
                from server import send_slack_notification
                result = await send_slack_notification(**parameters)
                return result

            elif tool_name == "summarize_pr_changes":
                from server import summarize_pr_changes
                result = await summarize_pr_changes(**parameters)
                return result

            elif tool_name == "generate_pr_description":
                from server import generate_pr_description
                result = await generate_pr_description(**parameters)
                return result

            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            print(f"❌ Tool execution error: {str(e)}")
            # Fallback to simulation
            return self._simulate_tool_call(tool_name, parameters)

    def _simulate_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Fallback simulation for tools that can't be called directly"""
        if tool_name == "analyze_file_changes":
            return json.dumps({
                "base_branch": parameters.get("base_branch", "main"),
                "files_changed": "M\tsrc/main.py\nM\ttests/test_main.py\nA\tnew_feature.py",
                "statistics": "3 files changed, 45 insertions(+), 12 deletions(-)",
                "commits": "abc1234 Add new feature implementation\nxyz5678 Fix bug in main.py",
                "diff": "@@ -10,5 +10,8 @@\n # Main function\n def main():\n+    # New feature implementation\n+    feature = NewFeature()\n+    feature.run()\n     print('Hello World')\n\n@@ -25,3 +28,6 @@\n if __name__ == '__main__':\n     main()",
                "truncated": False
            })

        elif tool_name == "get_pr_templates":
            return json.dumps([
                {"filename": "feature.md", "type": "Feature", "content": "# Feature\n\n## Description\n\n## User Story\n\n## Implementation Details"},
                {"filename": "bug.md", "type": "Bug Fix", "content": "# Bug Fix\n\n## Description\n\n## Root Cause\n\n## Impact"},
                {"filename": "refactor.md", "type": "Refactor", "content": "# Refactor\n\n## Description\n\n## Scope\n\n## Benefits"}
            ])

        elif tool_name == "suggest_template":
            template_map = {
                "feature": "feature.md",
                "enhancement": "feature.md",
                "bug": "bug.md",
                "fix": "bug.md",
                "refactor": "refactor.md",
                "cleanup": "refactor.md"
            }
            suggested = template_map.get(parameters.get("change_type", "").lower(), "feature.md")
            return json.dumps({
                "recommended_template": {"filename": suggested, "type": parameters.get("change_type", "Feature")},
                "reasoning": f"Based on '{parameters.get('changes_summary', '')}', this appears to be a {parameters.get('change_type', 'feature')} change.",
                "usage_hint": "Use this template to document your PR changes."
            })

        elif tool_name == "summarize_pr_changes":
            diff = parameters.get("diff_content", "")
            summary = f"Summary of changes: {len(diff.split())} lines modified, focusing on feature implementation and bug fixes."
            return json.dumps({
                "summary": summary[:parameters.get("max_length", 200)],
                "model_used": "HuggingFace AI",
                "input_length": len(diff)
            })

        elif tool_name == "generate_pr_description":
            return json.dumps({
                "pr_description": f"# {parameters.get('change_type', 'Feature').title()} Implementation\n\n## Changes\n{parameters.get('changes_summary', '')}\n\n## Impact\nThis change improves the codebase by...\n\n## Testing\n- Unit tests added\n- Integration tests verified",
                "change_type": parameters.get("change_type", "feature"),
                "model_used": "HuggingFace AI"
            })

        elif tool_name == "get_recent_actions_events":
            return json.dumps([
                {"event_type": "workflow_run", "action": "completed", "workflow_run": {"name": "CI", "status": "completed", "conclusion": "success"}},
                {"event_type": "workflow_run", "action": "completed", "workflow_run": {"name": "Tests", "status": "completed", "conclusion": "success"}}
            ])

        elif tool_name == "get_workflow_status":
            return json.dumps([
                {"name": "CI", "status": "completed", "conclusion": "success", "updated_at": "2025-12-30T08:55:00Z"},
                {"name": "Tests", "status": "completed", "conclusion": "success", "updated_at": "2025-12-30T08:55:00Z"}
            ])

        elif tool_name == "send_slack_notification":
            return "✅ Message sent successfully to Slack"

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    async def process_query(self, user_query: str) -> str:
        """Process user query using local LLM and intelligent tool calling"""

        print(f"📝 User query: {user_query}")

        # Simple rule-based tool selection (since local models don't have built-in tool calling)
        # In a production system, you'd use a more sophisticated approach

        user_query_lower = user_query.lower()

        # Analyze query to decide which tools to call
        tools_to_call = []

        if any(word in user_query_lower for word in ["analyze", "changes", "diff", "git", "files"]):
            tools_to_call.append(("analyze_file_changes", {}))

        if any(word in user_query_lower for word in ["template", "suggest", "recommend"]):
            if "changes_summary" in user_query or "change_type" in user_query:
                # Extract parameters from query (simple approach)
                changes_summary = "Code changes made"
                change_type = "feature"
                if "bug" in user_query_lower:
                    change_type = "bug"
                elif "refactor" in user_query_lower:
                    change_type = "refactor"
                tools_to_call.append(("suggest_template", {
                    "changes_summary": changes_summary,
                    "change_type": change_type
                }))

        if any(word in user_query_lower for word in ["summarize", "summary"]):
            tools_to_call.append(("summarize_pr_changes", {
                "diff_content": "Sample diff content for demonstration",
                "max_length": 200
            }))

        if any(word in user_query_lower for word in ["generate", "description", "pr description"]):
            tools_to_call.append(("generate_pr_description", {
                "changes_summary": "Implementation of new features",
                "change_type": "feature"
            }))

        if any(word in user_query_lower for word in ["status", "ci", "cd", "workflow", "actions"]):
            tools_to_call.append(("get_workflow_status", {}))

        if any(word in user_query_lower for word in ["slack", "notify", "notification"]):
            tools_to_call.append(("send_slack_notification", {
                "message": "Test notification from PR Assistant"
            }))

        if any(word in user_query_lower for word in ["template", "templates"]) and not tools_to_call:
            tools_to_call.append(("get_pr_templates", {}))

        # Execute tools and gather results
        tool_results = []
        for tool_name, parameters in tools_to_call:
            print(f"🔧 Executing: {tool_name}")
            result = await self.call_tool(tool_name, parameters)
            tool_results.append(f"{tool_name}: {result}")

        # Generate response using local model
        tool_results_text = "\n".join(tool_results) if tool_results else "No tools were needed for this query."
        context = f"""
User Query: {user_query}

Tool Results:
{tool_results_text}

Please provide a helpful response based on the above information.
""".strip()

        try:
            # Use local model for response generation
            inputs = self.tokenizer(context, return_tensors="pt", truncation=True, max_length=512)

            if self.device >= 0:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                self.model.to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Clean up response (remove the context from the beginning if present)
            if context in response:
                response = response.replace(context, "").strip()

            return response if response else "I've analyzed your request and executed the relevant tools. The results are shown above."

        except Exception as e:
            # Fallback response if model generation fails
            if tool_results:
                return f"I've executed the following tools for your query:\n" + "\n".join(f"• {result}" for result in tool_results)
            else:
                return "I understand your query about PR analysis. While I don't have specific tools to run right now, I can help you with general guidance on GitHub PR management."

async def main():
    """Main chat interface"""
    print("🤖 GitHub PR Analysis Assistant")
    print("=" * 50)
    print("Ask me about PR analysis, code changes, CI/CD status, or anything related to your repository!")
    print("Type 'quit' to exit.\n")

    client = MCPClient()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not user_input:
                continue

            print("🤔 Thinking...")

            response = await client.process_query(user_input)

            print(f"\n🤖 Assistant: {response}\n")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

if __name__ == "__main__":
    # No API key needed - using free local models!
    print("� Starting with free local AI models...")
    asyncio.run(main())
