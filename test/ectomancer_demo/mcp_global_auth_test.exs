defmodule EctomancerDemo.MCPGlobalAuthTest do
  use ExUnit.Case

  describe "EctomancerDemo.MCP with global auth" do
    test "global auth allows admin" do
      alias EctomancerDemo.MCP.Tool.ListUsers

      frame = %{assigns: %{ectomancer_actor: %{role: :admin}}}
      result = ListUsers.execute(%{}, frame)

      # Admin should pass auth (error about missing query params is expected)
      assert {:error, error, _} = result
      refute error.message =~ "Unauthorized"
    end

    test "global auth denies non-admin" do
      alias EctomancerDemo.MCP.Tool.ListUsers

      frame = %{assigns: %{ectomancer_actor: %{role: :user}}}
      assert {:error, error, _} = ListUsers.execute(%{}, frame)
      assert error.code == -32_001
      assert error.message =~ "Unauthorized"
    end

    test "global auth rejects actor without role" do
      alias EctomancerDemo.MCP.Tool.ListUsers

      frame = %{assigns: %{ectomancer_actor: %{}}}
      assert {:error, error, _} = ListUsers.execute(%{}, frame)
      assert error.code == -32_001
      assert error.message =~ "Unauthorized"
    end

    test "all schemas inherit global auth" do
      alias EctomancerDemo.MCP.Tool.ListPosts
      alias EctomancerDemo.MCP.Tool.ListComments
      alias EctomancerDemo.MCP.Tool.CreateUser
      alias EctomancerDemo.MCP.Tool.UpdateUser
      alias EctomancerDemo.MCP.Tool.DestroyUser

      user_frame = %{assigns: %{ectomancer_actor: %{role: :user}}}

      # All list tools deny non-admin
      assert {:error, error, _} = ListPosts.execute(%{}, user_frame)
      assert error.code == -32_001

      assert {:error, error, _} = ListComments.execute(%{}, user_frame)
      assert error.code == -32_001

      # Mutations also deny non-admin
      assert {:error, error, _} = CreateUser.execute(%{"email" => "x@x.com", "name" => "X"}, user_frame)
      assert error.code == -32_001

      assert {:error, error, _} = UpdateUser.execute(%{"id" => "1"}, user_frame)
      assert error.code == -32_001

      assert {:error, error, _} = DestroyUser.execute(%{"id" => "1"}, user_frame)
      assert error.code == -32_001
    end
  end
end
