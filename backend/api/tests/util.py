import urllib

# return author id that is escaped
def get_author_id(host, input_id, escaped):
    formated_id = "{}author/{}".format(host, str(input_id))
    if(escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id
