from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from .models.authorModel import Author
from rest_framework import status
import base64, requests, json

def getPageNumber(request, number=1):
  try:  # try to get the `page` query parameter
    page = int(request.query_params['page'])
  except:  # set `page` to `1` if something goes wrong
    page = number
  
  # return the page number
  return page

def getPageSize(request, size=10):
  try:  # try to get the `size` query parameter
    page_size = int(request.query_params['size'])
  except:  # set `size` to `10` if something goes wrong
    page_size = size
  
  # return the page size
  return page_size

def getPaginatedObject(object, page, page_size):
  
  try:  # try to get the paginated object
    paginator = Paginator(object, page_size)
    paginated_object = paginator.page(page)
  except EmptyPage:  # get the last non-empty page if the requested page is empty
    paginated_object = paginator.page(paginator.num_pages)
  
  # return the paginated object
  return paginated_object

def handlePostImage(body):
  # check if the request body has a content type
  if hasattr(body, 'contentType'):
    try:  # try to handle the image if it exists
      contentType = body["contentType"]
      
      # if the content type is an image
      if (contentType.startswith("image/")):
        content = body["content"]
        
        # base64 encode the image
        if not content.startswith("data:image/"):
          url = content
          base64Img = base64.b64encode(requests.get(url).content).decode("utf-8")
          body["content"] = "data:" + contentType + "," + base64Img
    
    except:  # raise an error if something goes wrong
      raise ValueError('Image handling went wrong.')
  
  # return the request body
  return body

def loggedInUserExists(request):
  try:  # try to get the logged in author
    logged_in_author_uuid = request.user.uuid
    Author.objects.get(uuid=logged_in_author_uuid)
  except:  # return an error if something goes wrong
    return False
  
  return True

def loggedInUserIsAuthor(request, author_uuid):
  try:  # try to get the logged in author
    logged_in_author_uuid = request.user.uuid
    Author.objects.get(uuid=logged_in_author_uuid)
  except:  # return an error if something goes wrong
    return False
  
  # if the logged in author isn't the author
  if str(logged_in_author_uuid) != str(author_uuid):
    return False
  
  return True

def loggedInUserHasId(request, author_id):
  try:  # try to get the logged in author
    logged_in_author_uuid = request.user.uuid
    loggedInAuthorObject = Author.objects.get(uuid=logged_in_author_uuid)
    authorObject = Author.objects.get(id=author_id)
  except:  # return an error if something goes wrong
    return False
  
  # if the logged in author isn't the author
  if loggedInAuthorObject.id != authorObject.id:  
    return False
  
  return True

def getLoggedInAuthorUUID(request):
  try:  # try to get the logged in author
    logged_in_author_uuid = request.user.uuid
    Author.objects.get(uuid=logged_in_author_uuid)
  except:  # return an error if something goes wrong
    return None
  
  return logged_in_author_uuid

def getLoggedInAuthorObject(request):
  try:  # try to get the logged in author
    logged_in_author_uuid = request.user.uuid
    loggedInAuthorObject = Author.objects.get(uuid=logged_in_author_uuid)
  except:  # return an error if something goes wrong
    return None
  
  return loggedInAuthorObject

def postToAuthorInbox(request, data, receiver_author_uuid):
  try:
    url = 'http://127.0.0.1:8000/service/author/' + receiver_author_uuid + '/inbox'
    payload = data
    sender_author_authorization = request.headers['Authorization']
    headers = {'content-type': 'application/json', 'Authorization': sender_author_authorization}
    requests.post(url, data=json.dumps(payload), headers=headers)
  except:  # raise an error if something goes wrong
      raise ValueError('Posting to Inbox went wrong.')
