#!/bin/bash
# Ectomancer MCP Demo Script
set -e

MCP_URL="http://127.0.0.1:4000/mcp"

echo "╔══════════════════════════════════════════════════╗"
echo "║     🧙 Ectomancer MCP Demo - v1.2.1              ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Step 1: Show the MCP module source
echo "━━━ Step 1: MCP Module ━━━"
echo "Showing the Ectomancer schema declarations..."
echo ""

cat lib/ectomancer_demo/mcp.ex
echo ""
echo ""

# Wait for server
sleep 2

# Step 2: Initialize MCP session
echo "━━━ Step 2: Initialize ━━━"
echo "Establishing MCP session..."
echo ""

INIT_RESP=$(curl -s -w "\n%{http_code}" -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "mcp-session-id: demo-001" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "demo-client", "version": "1.0.0"}
    }
  }')

echo "$INIT_RESP" | head -1 | python3 -m json.tool 2>/dev/null || echo "$INIT_RESP" | head -1
echo ""
sleep 1

# Step 3: List Tools
echo "━━━ Step 3: tools/list ━━━"
echo "Discovering auto-generated MCP tools..."
echo ""

TOOLS_RESP=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "mcp-session-id: demo-001" \
  -d '{
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/list",
    "params": {}
  }')

echo "$TOOLS_RESP" | python3 -c "
import json, sys
data = json.load(sys.stdin)
tools = data.get('result', {}).get('tools', [])
print(f'Found {len(tools)} tools:')
for t in tools:
    print(f'  📍 {t[\"name\"]}: {t.get(\"description\", \"\")[:80]}')
" 2>/dev/null || echo "$TOOLS_RESP"
echo ""
sleep 1

# Step 4: List Users
echo "━━━ Step 4: list_users ━━━"
echo "Querying all users..."
echo ""

USERS_RESP=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "mcp-session-id: demo-001" \
  -d '{
    "jsonrpc": "2.0",
    "id": "3",
    "method": "tools/call",
    "params": {
      "name": "list_users",
      "arguments": {}
    }
  }')

echo "$USERS_RESP" | python3 -m json.tool 2>/dev/null
echo ""
sleep 1

# Step 5: Create User
echo "━━━ Step 5: create_user ━━━"
echo "Creating a new user 'Diana'..."
echo ""

CREATE_RESP=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "mcp-session-id: demo-001" \
  -d '{
    "jsonrpc": "2.0",
    "id": "4",
    "method": "tools/call",
    "params": {
      "name": "create_user",
      "arguments": {
        "user": {
          "name": "Diana",
          "email": "diana@example.com"
        }
      }
    }
  }')

echo "$CREATE_RESP" | python3 -m json.tool 2>/dev/null
echo ""
sleep 1

# Step 6: List posts
echo "━━━ Step 6: list_posts (with filter) ━━━"
echo "Searching posts with title containing 'hello'..."
echo ""

POSTS_RESP=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "mcp-session-id: demo-001" \
  -d '{
    "jsonrpc": "2.0",
    "id": "5",
    "method": "tools/call",
    "params": {
      "name": "list_posts",
      "arguments": {
        "title_contains": "hello"
      }
    }
  }')

echo "$POSTS_RESP" | python3 -m json.tool 2>/dev/null
echo ""

echo "╔══════════════════════════════════════════════════╗"
echo "║     ✅ Demo Complete!                            ║"
echo "╚══════════════════════════════════════════════════╝"
