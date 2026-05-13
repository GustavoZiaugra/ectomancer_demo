#!/usr/bin/env python3
"""Ectomancer MCP Demo - Beautiful terminal recording"""
import json
import sys
import time
import textwrap
from datetime import datetime

import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.layout import Layout
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
from rich import box

console = Console()
MCP_URL = "http://127.0.0.1:4000/mcp"
SESSION_ID = "demo-001"
client = httpx.Client(timeout=10)

def mcp_call(method, params=None):
    """Make MCP request and return parsed response."""
    body = {
        "jsonrpc": "2.0",
        "id": str(int(time.time() * 1000)),
        "method": method,
        "params": params or {}
    }
    resp = client.post(
        MCP_URL,
        json=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "mcp-session-id": SESSION_ID
        }
    )
    return resp.json()

def step(title, delay=0.8):
    """Print a step header."""
    console.print()
    console.print(Rule(f"[bold cyan]{title}", style="blue"))
    time.sleep(0.3)

def show_code(path, language="elixir", title=None):
    """Show syntax-highlighted code from a file."""
    try:
        with open(path) as f:
            code = f.read()
    except:
        code = f"# File not found: {path}"
    
    syntax = Syntax(code, language, theme="monokai", line_numbers=True, word_wrap=True)
    if title:
        console.print(Panel(syntax, title=title, border_style="green"))
    else:
        console.print(syntax)
    time.sleep(0.5)

def show_json(data, title=None):
    """Show formatted JSON response."""
    formatted = json.dumps(data, indent=2, ensure_ascii=False)
    syntax = Syntax(formatted, "json", theme="monokai", word_wrap=True)
    if title:
        console.print(Panel(syntax, title=title, border_style="yellow"))
    else:
        console.print(syntax)

def show_tools_table(tools):
    """Show tools in a beautiful table."""
    table = Table(title="[bold]🛠️  Auto-Generated MCP Tools", box=box.ROUNDED, 
                  header_style="bold magenta", title_style="bold cyan")
    table.add_column("Tool", style="cyan", width=22)
    table.add_column("Description", style="white", width=50)
    table.add_column("Actions", style="green", width=20)
    
    for t in tools:
        desc = t.get("description", "").split(".")[0][:48]
        actions = t["name"].split("_")[0] if "_" in t["name"] else "all"
        table.add_row(t["name"], desc, actions)
    
    console.print(table)

def show_users_table(users, title="Users"):
    """Show users in a table."""
    table = Table(title=f"[bold]{title}", box=box.SIMPLE, header_style="bold cyan")
    if not users:
        console.print("[yellow]No users found[/yellow]")
        return
    
    # Infer columns from first user
    for key in users[0].keys():
        table.add_column(key.capitalize(), style="white", overflow="fold")
    
    for user in users:
        table.add_row(*[str(v) for v in user.values()])
    
    console.print(table)

def type_text(text, speed=0.03):
    """Simulate typing by printing character by character (for asciicast recording)."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

# ========== DEMO START ==========

console.clear()
console.print()
console.print(Panel.fit(
    "[bold cyan]🧙  Ectomancer MCP Demo[/bold cyan]\n"
    "[white]v1.2.1 — Auto-generated MCP tools from Ecto schemas[/white]\n\n"
    "[dim]This demo shows how Ectomancer automatically exposes\n"
    "Phoenix/Ecto schemas as MCP tools with zero boilerplate.[/dim]",
    border_style="cyan", box=box.DOUBLE_EDGE, padding=(1, 4)
))
time.sleep(1.5)

# Step 1: Show the MCP module
step("Step 1: The MCP Module — Just 12 Lines")
console.print(
    "[dim]Ectomancer generates all CRUD tools from a simple declaration.[/dim]\n"
    "[dim]Each schema becomes tools like list_users, create_post, etc.[/dim]"
)
time.sleep(0.5)
show_code("lib/ectomancer_demo/mcp.ex", "elixir", 
          "lib/ectomancer_demo/mcp.ex — The entire MCP configuration")
time.sleep(1)

# Step 2: Show the Router
step("Step 2: Router Integration")
console.print("[dim]A single line in your Phoenix router mounts the MCP endpoint.[/dim]")
time.sleep(0.3)
show_code("lib/ectomancer_demo_web/router.ex", "elixir",
          "lib/ectomancer_demo_web/router.ex — MCP forward at /mcp")
time.sleep(1)

# Step 3: Show the schemas
step("Step 3: Ecto Schemas — Your Data Model")
console.print("[dim]Ectomancer reads your Ecto schemas and generates tools automatically.[/dim]")
time.sleep(0.3)
show_code("lib/ectomancer_demo/user.ex", "elixir", "User Schema")
time.sleep(0.5)
show_code("lib/ectomancer_demo/post.ex", "elixir", "Post Schema")
time.sleep(0.5)

# Step 4: Initialize
step("Step 4: Initialize MCP Session")
console.print("[dim]Establishing connection to the MCP server...[/dim]")
time.sleep(0.5)

init_resp = mcp_call("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "demo", "version": "1.0.0"}
})

show_json(init_resp, "initialize response")
time.sleep(1)

# Step 5: List Tools
step("Step 5: Discover All MCP Tools")

console.print("[dim]Ectomancer generated [bold cyan]15 tools[/bold cyan] from 3 schemas![/dim]")
time.sleep(0.5)

tools_resp = mcp_call("tools/list")
tools = tools_resp.get("result", {}).get("tools", [])
show_tools_table(tools)
time.sleep(1.5)

# Step 6: List Users
step("Step 6: Query All Users — list_users")

console.print("[dim]Each tool accepts filters based on schema fields.[/dim]")
time.sleep(0.5)

users_resp = mcp_call("tools/call", {
    "name": "list_users",
    "arguments": {}
})

users = users_resp.get("result", {}).get("content", [{}])[0].get("text", "[]")
try:
    users_data = json.loads(users)
    show_users_table(users_data, "list_users — 3 seeded users found")
except (json.JSONDecodeError, IndexError, KeyError):
    show_json(users_resp, "list_users response")
time.sleep(1)

# Step 7: Create User
step("Step 7: Create a New User — create_user")

console.print("[dim]Ectomancer validates input against the Ecto schema.[/dim]")
time.sleep(0.3)

create_resp = mcp_call("tools/call", {
    "name": "create_user",
    "arguments": {
        "user": {
            "name": "Diana Prince",
            "email": "diana@example.com",
            "bio": "Amazonian warrior and superhero"
        }
    }
})
show_json(create_resp, "create_user — Diana created successfully ✅")
time.sleep(1)

# Step 8: Get specific user
step("Step 8: Get User by ID — get_user")

console.print("[dim]Read a specific record by primary key.[/dim]")
time.sleep(0.3)

get_resp = mcp_call("tools/call", {
    "name": "get_user",
    "arguments": {"id": 1}
})
show_json(get_resp, "get_user — User #1 details")
time.sleep(1)

# Step 9: Filtered Post Search
step("Step 9: Advanced Filtering — list_posts with title_contains")

console.print("[dim]String fields get automatic [bold]LIKE[/bold] filters.[/dim]")
time.sleep(0.3)

posts_resp = mcp_call("tools/call", {
    "name": "list_posts",
    "arguments": {"title_contains": "hello"}
})
show_json(posts_resp, "list_posts — Filtered by title containing 'hello'")
time.sleep(1)

# Step 10: Create Post
step("Step 10: Create a Post with Associations")

create_post_resp = mcp_call("tools/call", {
    "name": "create_post",
    "arguments": {
        "post": {
            "title": "Ectomancer is Awesome!",
            "body": "This post was created entirely through an MCP tool call.",
            "user_id": 1
        }
    }
})
show_json(create_post_resp, "create_post — New post created ✅")
time.sleep(1)

# Step 11: Update User
step("Step 11: Update a User — update_user")

console.print("[dim]Update specific fields, keeping existing data intact.[/dim]")
time.sleep(0.3)

update_resp = mcp_call("tools/call", {
    "name": "update_user",
    "arguments": {
        "id": 4,
        "user": {"email": "diana.prince@themyscira.com"}
    }
})
show_json(update_resp, "update_user — Diana's email updated")
time.sleep(1)

# Step 12: Summary
step("Final: What We've Seen", delay=0.5)

console.print(Panel.fit(
    "[bold green]✅  Ectomancer in Action[/bold green]\n\n"
    "[cyan]• 3 Ecto schemas[/cyan] → [white]15 MCP tools[/white] (list, get, create, update, destroy)\n"
    "[cyan]•[/cyan] [white]Zero boilerplate[/white] — just [bold]use Ectomancer[/bold] + [bold]expose[/bold]\n"
    "[cyan]•[/cyan] [white]Automatic validation[/white] via Ecto changesets\n"
    "[cyan]•[/cyan] [white]Advanced filtering[/white] with LIKE operators on strings\n"
    "[cyan]•[/cyan] [white]Association support[/white] — create posts linked to users\n"
    "[cyan]•[/cyan] [white]Streamable HTTP[/white] transport — MCP 2025-03-26 compliant\n\n"
    "[dim]All of this from just 3 lines of Elixir code per schema.[/dim]",
    border_style="green", box=box.ROUNDED, padding=(1, 2)
))

time.sleep(2)
console.print()
console.print("[bold]🔗  Learn more:[/bold] [underline]https://github.com/GustavoZiaugra/ectomancer[/underline]")
console.print()
