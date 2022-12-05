from webserver.models import Author, Post, Node

def create_local_author(username="local_author", display_name="local_author"):
    return Author.objects.create(username=username, display_name=display_name)

def create_local_post(
    author,
    title="Test Post",
    description="Testing post",
    source="",
    origin="",
    unlisted=False,
    content_type= "text/plain",
    content="Some content",
    visibility="PUBLIC"
):
    return Post.objects.create(
        author=author,
        title=title,
        description=description,
        source=source,
        origin=origin,
        unlisted=unlisted,
        content_type=content_type,
        content=content,
        visibility=visibility
    )

def create_remote_node(
    team,
    username="node_user",
    display_name="node_user",
    api_url="https://social-distribution-1.herokuapp.com/api"
):
    node_user = Author.objects.create(username=username, display_name=display_name, is_remote_user=True)
    node = Node.objects.create(
        api_url=api_url,
        team=team, 
        user=node_user,
        auth_username=f"team{team}",
        auth_password=f"team{team}"
    )
    return node
