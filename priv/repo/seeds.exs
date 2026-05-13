alias EctomancerDemo.Repo
alias EctomancerDemo.{User, Post, Comment}

alice = Repo.insert!(%User{name: "Alice", email: "alice@example.com"})
bob = Repo.insert!(%User{name: "Bob", email: "bob@example.com"})
carol = Repo.insert!(%User{name: "Carol", email: "carol@example.com"})

post1 = Repo.insert!(%Post{title: "Getting Started with MCP", body: "Model Context Protocol lets AI agents interact with your data...", user_id: alice.id})
post2 = Repo.insert!(%Post{title: "Elixir in Production", body: "Our journey running Phoenix at scale...", user_id: bob.id})
post3 = Repo.insert!(%Post{title: "Why SQLite is Underrated", body: "For many apps, SQLite is all you need...", user_id: alice.id})

Repo.insert!(%Comment{content: "Great post!", user_id: bob.id, post_id: post1.id})
Repo.insert!(%Comment{content: "Thanks for sharing", user_id: carol.id, post_id: post1.id})
Repo.insert!(%Comment{content: "We use Ecto with Postgres but this is interesting", user_id: carol.id, post_id: post3.id})
Repo.insert!(%Comment{content: "Could you share your deployment setup?", user_id: alice.id, post_id: post2.id})
