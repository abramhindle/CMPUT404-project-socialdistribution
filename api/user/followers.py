from api.app import app

# todo (matt): we need to come up with a format for communicating follow requests in between teams
@app.route('/authors/<string:author_id>/followers', methods=['GET'])
def followers(author_id: str):
    """get a list of authors who are AUTHOR_ID’s followers"""
    pass


@app.route('/authors/<string:author_id>/followers/{foreign_author_id}', methods=['DELETE'])
def remove_follower(author_id: str):
    """remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID"""
    pass


@app.route('/authors/<string:author_id>/followers/{foreign_author_id}', methods=['PUT'])
def add_follower(author_id: str):
    """Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)"""
    pass


@app.route('/authors/<string:author_id>/followers/{foreign_author_id}', methods=['GET'])
def check_is_follower(author_id: str):
    """check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID"""
    pass
