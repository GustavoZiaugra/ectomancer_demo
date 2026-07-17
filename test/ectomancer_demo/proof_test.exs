defmodule EctomancerDemo.ProofTest do
  use ExUnit.Case

  test "PROOF: global auth works end-to-end" do
    alias EctomancerDemo.MCP.Tool.{ListUsers, CreateUser, GetUser, UpdateUser, DestroyUser}
    alias EctomancerDemo.MCP.Tool.{ListPosts, ListComments}

    admin  = %{assigns: %{ectomancer_actor: %{role: :admin}}}
    user   = %{assigns: %{ectomancer_actor: %{role: :user}}}
    norole = %{assigns: %{ectomancer_actor: %{}}}

    # ── Admin passes auth (gets non-auth error, repo hits the handler) ──
    assert {:error, error, _} = ListUsers.execute(%{}, admin)
    refute error.message =~ "Unauthorized"

    # ── User denied across ALL schemas and actions ──
    for {label, mod} <- [
      {"ListUsers",    ListUsers},
      {"GetUser",      GetUser},
      {"CreateUser",   CreateUser},
      {"UpdateUser",   UpdateUser},
      {"DestroyUser",  DestroyUser},
      {"ListPosts",    ListPosts},
      {"ListComments", ListComments},
    ] do
      assert {:error, error, _} = mod.execute(%{}, user),
             "#{label}: expected denial for user"
      assert error.code == -32_001, "#{label}: wrong code #{error.code}"
      assert error.message =~ "Unauthorized", "#{label}: wrong message"
    end

    # ── No role → denied ──
    assert {:error, error, _} = ListUsers.execute(%{}, norole)
    assert error.code == -32_001
  end
end
