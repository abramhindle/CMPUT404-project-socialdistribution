import urllib

# return author id that is escaped
def get_author_id(host, input_id):
    formated_id = "{}author/{}".format(host, str(input_id))
    escaped_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return escaped_id
