defmodule EctomancerDemo.Repo do
  use Ecto.Repo,
    otp_app: :ectomancer_demo,
    adapter: Ecto.Adapters.SQLite3
end
