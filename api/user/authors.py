from flask import Blueprint

from api.utils import get_pagination_params

# note: this blueprint is usually mounted under /authors URL prefix
authors_bp = Blueprint("authors", __name__)


@authors_bp.route("/", methods=["GET"])
def get_authors():
    pagination = get_pagination_params()
    return {"hello": 1}


@authors_bp.route("/<string:author_id>", methods=["GET"])
def get_single_author(author_id: str):
    pass
