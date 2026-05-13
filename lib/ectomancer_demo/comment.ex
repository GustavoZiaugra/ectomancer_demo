defmodule EctomancerDemo.Comment do
  use Ecto.Schema
  import Ecto.Changeset

  schema "comments" do
    field :content, :string
    belongs_to :user, EctomancerDemo.User
    belongs_to :post, EctomancerDemo.Post

    timestamps()
  end

  def changeset(comment, attrs) do
    comment
    |> cast(attrs, [:content, :user_id, :post_id])
    |> validate_required([:content, :user_id, :post_id])
    |> assoc_constraint(:user)
    |> assoc_constraint(:post)
  end
end
