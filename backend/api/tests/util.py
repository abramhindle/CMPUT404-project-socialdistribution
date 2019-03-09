def get_author_id(author_profile):
    return "{}author/{}".format(author_profile.host, str(author_profile.id))
