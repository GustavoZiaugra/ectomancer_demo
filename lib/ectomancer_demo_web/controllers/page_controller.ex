defmodule EctomancerDemoWeb.PageController do
  use EctomancerDemoWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
