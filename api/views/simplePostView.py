from rest_framework.decorators import api_view

from ..services.postServices import postServices


#########################################
# post request, asking for 
#    title, str
#    author_id, uuid
#    description, str
#    content, str
#    visibility, str
#
# return: None
##########################################
@api_view(['POST'])
def createNewPost(request, author_id):
  request.data['author_id'] = author_id
  res = postServices.creatNewPost(request)
  return res

############################################
# request: get, post
#
# args: author_id and post_id
#
# return query result in json list
################################################
@api_view(['GET', 'PUT'])
def handleExistPost(request, author_id, post_id):
  try:
    if request.method == 'GET':
      # make sure author id matches
      res = getPost(request, author_id, post_id)
      return res

  except AssertionError:
    raise NotImplementedError("some Http method is not implemented for this api point")


def getPost(request, author_id, post_id):
  res = postServices.getPostById(request, post_id, author_id)
  return res

# method for same link goes down to here
# post, delete, put

#############################################
# please implement next post related api point here
# if needed
#
############################################