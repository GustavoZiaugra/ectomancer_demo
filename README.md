# Ectomancer Demo

A tiny Phoenix app with three Ecto schemas — `User`, `Post`, and `Comment` — exposed as MCP tools by [Ectomancer](https://github.com/GustavoZiaugra/ectomancer).

**3 schemas → 15+ MCP tools** (`list`, `get`, `create`, `update`, `destroy`, plus batch operations) with no hand-written tool definitions.

> This demo is intentionally permissive so you can try writes. Do not copy its authorization config into production.

## Run it

Requirements: Elixir 1.18+, Erlang/OTP 27+, and SQLite (bundled via `ecto_sqlite3`).

```bash
git clone https://github.com/GustavoZiaugra/ectomancer_demo
cd ectomancer_demo
mix setup
mix phx.server
```

`mix setup` installs dependencies, creates the SQLite database, runs migrations, and seeds fake users/posts/comments.

The MCP endpoint is:

```
http://localhost:4000/mcp
```

## Connect Claude

### Claude Code

```bash
claude mcp add --transport http ectomancer-demo http://localhost:4000/mcp
```

Then ask Claude to use the `ectomancer-demo` tools.

### Claude Desktop

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ectomancer-demo": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:4000/mcp"]
    }
  }
}
```

Restart Claude Desktop after saving the file.

### Any MCP client

Use the Streamable HTTP transport and point it at `http://localhost:4000/mcp`.

## Try these prompts

- “List all users.”
- “Show me the 5 most recent posts and their authors.”
- “Create a post for Alice titled ‘Hello MCP’ with the body ‘Testing Ectomancer’.”
- “Find posts whose title contains ‘MCP’ and show their comments.”
- “Who commented on ‘Getting Started with MCP’?”
- “Create a comment from Bob on the newest post.”

## What is exposed

`lib/ectomancer_demo/mcp.ex` is the whole integration:

```elixir
defmodule EctomancerDemo.MCP do
  use Ectomancer,
    name: "ectomancer-demo",
    version: "1.0.0",
    authorize: fn actor, _action -> Map.get(actor, :role) == :admin end

  expose EctomancerDemo.User,
    actions: [:list, :get, :create, :update, :destroy]

  expose EctomancerDemo.Post,
    actions: [:list, :get, :create, :update, :destroy]

  expose EctomancerDemo.Comment,
    actions: [:list, :get, :create, :update, :destroy]
end
```

The demo’s `config/runtime.exs` makes every request an admin so writes work without a login screen:

```elixir
config :ectomancer,
  repo: EctomancerDemo.Repo,
  actor_from: fn _conn -> %{role: :admin} end
```

In a real app, `actor_from` would extract the current user from the connection and `authorize` would enforce your own rules.

## Learn more

- [Ectomancer README](https://github.com/GustavoZiaugra/ectomancer)
- [Ectomancer on Hex](https://hex.pm/packages/ectomancer)
- [Ectomancer docs](https://hexdocs.pm/ectomancer)
