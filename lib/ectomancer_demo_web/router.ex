defmodule EctomancerDemoWeb.Router do
  use EctomancerDemoWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {EctomancerDemoWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", EctomancerDemoWeb do
    pipe_through :browser

    get "/", PageController, :home
  end

  scope "/api", EctomancerDemoWeb do
    pipe_through :api
  end

  scope "/mcp" do
    pipe_through :api
    forward "/", Ectomancer.Plug, server: EctomancerDemo.MCP
  end
end
