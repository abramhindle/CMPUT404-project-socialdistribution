from api.utils import get_pagination_params
from flask import Blueprint

authors_bp = Blueprint("authors", __name__)


@authors_bp.route("/authors", methods=['GET'])
def get_authors():
    pagination = get_pagination_params()
    return {"hello": 1}


@authors_bp.route('/authors/<string:author_id>', methods=['GET'])
def get_single_author(author_id: str):
    pass
