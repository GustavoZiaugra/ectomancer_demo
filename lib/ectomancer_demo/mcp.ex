defmodule EctomancerDemo.MCP do
  use Ectomancer,
    name: "ectomancer-demo",
    version: "1.0.0"

  expose EctomancerDemo.User,
    actions: [:list, :get, :create, :update, :destroy]

  expose EctomancerDemo.Post,
    actions: [:list, :get, :create, :update, :destroy]

  expose EctomancerDemo.Comment,
    actions: [:list, :get, :create, :update, :destroy]
end
