from api.utils import get_pagination_params
from api.app import app


@app.route("/authors", methods=['GET'])
def get_authors():
    pagination = get_pagination_params()
    return {"hello": 1}


@app.route('/authors/<string:author_id>', methods=['GET'])
def get_single_author(author_id: str):
    pass
