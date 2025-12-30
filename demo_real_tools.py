#!/usr/bin/env python3
"""
Demo script to show that the LLM client actually calls real MCP tools
"""

import asyncio
import json
from llm_client import MCPClient

async def demo_real_tools():
    """Demonstrate that tools are actually called"""

    print("🚀 Demo: LLM Client Actually Calling Real MCP Tools")
    print("=" * 60)

    client = MCPClient()

    # Test each tool directly
    test_cases = [
        ("get_pr_templates", {}, "Get PR templates"),
        ("get_recent_actions_events", {"limit": 5}, "Get recent GitHub Actions events"),
        ("get_workflow_status", {}, "Get workflow status"),
        ("send_slack_notification", {"message": "Demo: Tool is working!"}, "Send Slack notification"),
    ]

    print("Testing direct tool calls:\n")

    for tool_name, params, description in test_cases:
        print(f"🔧 Testing: {description}")
        try:
            result = await client.call_tool(tool_name, params)
            print(f"✅ Success: {result[:100]}..." if len(result) > 100 else f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print()

    print("Testing LLM-driven tool selection:\n")

    # Test LLM selecting tools based on queries
    test_queries = [
        "show me the available PR templates",
        "what's the status of our CI workflows",
        "send a notification to the team",
    ]

    for query in test_queries:
        print(f"💬 Query: '{query}'")
        try:
            response = await client.process_query(query)
            print(f"🤖 Response: {response[:150]}..." if len(response) > 150 else f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_real_tools())
