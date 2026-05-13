#!/usr/bin/env python3
"""Simple MCP SSE client for demo purposes."""
import httpx
import json
import sys
import time
import threading
import uuid

BASE_URL = "http://127.0.0.1:4000/mcp"

def interact():
    client = httpx.Client(timeout=30)
    
    # 1. Connect to SSE and get session_id
    print("🚀 Connecting to Ectomancer MCP server...")
    response = client.get(f"{BASE_URL}/sse")
    # The SSE response should have session_id in headers or initial data
    
    # Better approach: use streaming for SSE
    session_id = None
    messages_queue = []
    
    def read_sse():
        nonlocal session_id
        with httpx.Client(timeout=None) as sse_client:
            with sse_client.stream("GET", f"{BASE_URL}/sse") as resp:
                for line in resp.iter_lines():
                    line = line.strip()
                    if line.startswith("data:"):
                        data = line[5:].strip()
                        try:
                            msg = json.loads(data)
                            if "session_id" in msg:
                                session_id = msg["session_id"]
                            messages_queue.append(msg)
                        except:
                            pass
    
    sse_thread = threading.Thread(target=read_sse, daemon=True)
    sse_thread.start()
    time.sleep(1)
    
    if not session_id:
        print("❌ Could not get session_id from SSE")
        return
    
    print(f"✅ Connected! Session: {session_id}\n")
    
    def send_request(method, params=None):
        req_id = str(uuid.uuid4())[:8]
        body = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {}
        }
        print(f">>> {method}")
        resp = client.post(
            f"{BASE_URL}/message?session_id={session_id}",
            json=body
        )
        time.sleep(0.5)
        # Check SSE queue for response
        for msg in list(messages_queue):
            if isinstance(msg, dict) and msg.get("id") == req_id:
                return msg
        return None
    
    # 2. Initialize
    time.sleep(0.5)
    print("📡 Sending initialize...")
    client.post(
        f"{BASE_URL}/message?session_id={session_id}",
        json={
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "demo", "version": "1.0.0"}
            }
        }
    )
    time.sleep(1)
    print("✅ Initialized!\n")
    
    # 3. List tools
    print("🔧 Listing tools...")
    client.post(
        f"{BASE_URL}/message?session_id={session_id}",
        json={
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list",
            "params": {}
        }
    )
    time.sleep(1)
    # Print SSE messages received
    for msg in list(messages_queue):
        if isinstance(msg, dict):
            print(json.dumps(msg, indent=2)[:500])
    print()

if __name__ == "__main__":
    interact()
