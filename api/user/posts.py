from flask import Blueprint

from api.utils import get_pagination_params

# note: this blueprint is usually mounted under  URL prefix
posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/<string:author_id>/posts/<string:post_id>", methods=["GET"])
def get_post(author_id: str, post_id: str):
    """get the public post whose id is POST_ID"""
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>", methods=["POST"])
def edit_post(author_id: str, post_id: str):
    """update the post whose id is POST_ID (must be authenticated)"""
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>", methods=["DELETE"])
def delete_post(author_id: str, post_id: str):
    """remove the post whose id is post_id"""
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>", methods=["PUT"])
def create_post(author_id: str, post_id: str):
    """create a post where its id is post_id"""
    pass


@posts_bp.route("/<string:author_id>/posts", methods=["POST"])
def create_post_auto_gen_id(author_id: str):
    """create a new post but generate a new id"""
    pass


@posts_bp.route("/<string:author_id>/posts", methods=["GET"])
def get_recent_posts(author_id: str):
    """get the recent posts from author author_id (paginated)"""
    pagination = get_pagination_params()
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>/image", methods=["GET"])
def post_as_base64_img(author_id: str, post_id: str):
    """
    get the public post converted to binary as an image
     -> return 404 if not an image
    The end point decodes image posts as images. This allows the use of image tags in markdown.
    You can use this to proxy or cache images.
    """
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>/comments", methods=["GET"])
def get_comments(author_id: str, post_id: str):
    """get the list of comments of the post whose id is POST_ID (paginated)"""
    pagination = get_pagination_params()
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>/comments", methods=["POST"])
def post_comment(author_id: str, post_id: str):
    """if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID"""
    pass


@posts_bp.route("/<string:author_id>/inbox", methods=["POST"])
def send_like(author_id: str):
    """send a like object to author_id"""
    # todo (matt): why doesn't this have post id in the URL?
    pass


@posts_bp.route("/<string:author_id>/posts/<string:post_id>/likes", methods=["GET"])
def get_likes(author_id: str, post_id: str):
    """a list of likes from other authors on AUTHOR_ID’s post POST_ID"""
    pass


@posts_bp.route("/<string:author_id>/liked", methods=["GET"])
def get_author_likes(author_id: str):
    """
    list what public things AUTHOR_ID liked.

    It’s a list of of likes originating from this author
    Note: be careful here private information could be disclosed.
    """
    pass


@posts_bp.route("/<string:author_id>/inbox", methods=["GET"])
def get_inbox(author_id: str):
    """if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
    pagination = get_pagination_params()
    pass


@posts_bp.route("/<string:author_id>/inbox", methods=["POST"])
def post_inbox(author_id: str):
    """
    if the type is “post” then add that post to AUTHOR_ID’s inbox
    if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
    if the type is “like” then add that like to AUTHOR_ID’s inbox
    if the type is “comment” then add that comment to AUTHOR_ID’s inbox
    """
    pass


@posts_bp.route("/<string:author_id>/inbox", methods=["DELETE"])
def clear_inbox(author_id: str):
    """clear the inbox"""
    pass
