import pytest
from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get("posts/all")
    # print(res.json())

    def validate(post):
        """
        Posts validation using a schema, takes a
        list of dict >> a list of schema models
        """
        return schemas.PostOut(**post)

    mapped_test_posts = map(validate, res.json())
    posts_list = list(mapped_test_posts)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_one_post(client, test_posts):
    res = client.get(f"posts/{test_posts[0].id}")
    assert res.status_code == 200

    post = schemas.PostOut(**res.json())

    # Refer to scchemas
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

# def test_get_user_posts(client, test_posts, test_user):
#     res = client.get(f"posts/users/{test_user.id}")
#     assert res.status_code == 200

#     def validate(post):
#         """
#         Posts validation using a schema, takes a
#         list of dict >> a list of schema models
#         """
#         return schemas.PostOut(**post)

#     mapped_test_posts = map(validate, res.json())
#     posts_list = list(mapped_test_posts)

#     assert len(res.json()) == len(test_posts)
#     assert res.status_code == 200


def test_get_one_post_not_exist(client, test_posts):
    res = client.get(f"/posts/234")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("Intro to FastAPI", "test content 2", True),
        ("Writing Tests", "test content 2, Tests", False),
        ("What is Web 3.0? ", "test content 2 about web 3", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    new_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user["id"]


def test_create_post_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/",
        json={"title": "Test post published true", "content": "published?, yes"},
    )

    new_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert new_post.title == "Test post published true"
    assert new_post.content == "published?, yes"
    assert new_post.published == True
    assert new_post.owner_id == test_user["id"]


def test_create_post_unauthorized_user(client, test_user, test_posts):
    res = client.post(
        "/posts/",
        json={
            "title": "Test post Unauthorized user",
            "content": "Guest wants to create a post",
        },
    )

    assert res.status_code == 401


def test_delete_post_unauthorized_user(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_authorized_user(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8000000")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_update_post_unauthorized_user(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/000000", json=data)

    assert res.status_code == 404