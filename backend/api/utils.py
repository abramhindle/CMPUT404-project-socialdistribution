from django.core.paginator import Paginator, EmptyPage
import base64, requests

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
