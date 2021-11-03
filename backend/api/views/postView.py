from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.validators import URLValidator

from ..models import postModel
from ..serializers import PostSerializer
from .authorView import AuthorJSONID
from .commentView import commentMethod


from django.core import serializers
from django.core.paginator import Paginator
import json, base64, requests


@api_view(['POST', 'GET'])
def PostByAuthorID(request, authorID):
  try:
    if request.method == 'POST':
      result = createNewPostByAuthorID(request, authorID)
      return result
    elif request.method == 'GET':
      result = getAuthorID(request, authorID)
      return result
  except AssertionError:
    return Response(status=405)


def createNewPostByAuthorID(request, authorID):
  if request.data['visibility'] == 'Private':
    receiverURL = request.data['ReceiverURL']
    validate = URLValidator()
    try:
      validate(receiverURL)
      request.data['author'] = AuthorJSONID(authorID).data
      request.data['type'] = 'post'
      return Response(status=200)
    except:
      return Response(status=400)

  result = postMethod.createNewPost(request, authorID)
  return result

def getAuthorID(request, authorID, pageNumber = 1, pageSize = 1):
  result = postMethod.getPostByAuthorID(request, authorID)
  if 'size' in request.GET.keys():
    pageSize = request.GET.get('size')
  if 'page' in request.GET.keys():
    pageNumber = request.GET.get('page')
  if result.status_code == 404:
    return result
  return postMethod.postPagination(request, result, authorID, pageNumber, pageSize)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def PostByPostID(request, authorID, postID):
  try:
    if request.method == 'GET':
      # make sure author id matches
      result = getPost(request, authorID, postID)
      return result
    elif request.method == 'POST':
      result = editPost(request, authorID, postID)
      return result
      
    elif request.method == 'DELETE':
      result = deletePost(request, authorID)
      return result

  except AssertionError:
    return Response(status=405)


def getPost(request, authorID, postID):
  result = postMethod.PostByPostID(request, postID, authorID)
  if result.status_code == 404 or result.status_code == 403:
    return result
  formatedRes = postMethod.JSONFormatPost(request, result.data, authorID, postID)
  return formatedRes

def editPost(request):
  result = postMethod.editPostById(request)
  return result
  
def deletePost(request, authorID):
  result = postMethod.deletePostByPostId(request, authorID)
  return result

@api_view(['GET'])
def getStreamPosts(request, authorID, pageNumber = 1, pageSize = 1):
  if 'page' in request.GET.keys():
    pageNumber = request.GET.get('page')
  if 'size' in request.GET.keys():
    pageSize = request.GET.get('size')
  result = postMethod.VisiblePosts(request, authorID)
  if result.status_code == 404:
    return result
  return postMethod.postPagination(request, result, authorID, pageNumber, pageSize)









class postMethod():
  @staticmethod
  def editPostById(request):
    body = request.body.decode('utf-8')
    body = json.loads(body)
    url = request.build_absolute_uri()
    try:
      url = request.build_absolute_uri()
      data = postModel.Post.objects.get(url=url)
    except:
      return Response(status=400)

    if "contentType" in body:
      contentType = body["contentType"]
      if (contentType.startswith("image/")):
        content = body["content"]
        if not content.startswith("data:image/"):
          url = content
          base64Img = base64.b64encode(requests.get(url).content).decode("utf-8")
          body["content"] = "data:" + contentType + "," + base64Img
    try:
      for key in body:
        value = body.get(key, None)
        setattr(data, key, value)
      data.save()
      result = Response(status=200)
      result.data = body
      return result
    except:
      return Response(status=400)



  @staticmethod
  def createNewPost(request, authorID):
    request.data['postAuthorID'] = authorID
    serializer = PostSerializer(data=request.data)
    print(serializer,'serializer')
    if serializer.is_valid():
      contextInstance = serializer.save()
      contextInstance.url = request.build_absolute_uri() + str(contextInstance.postID)
      contextInstance.postURL = str(contextInstance.postID)
      if 'source' in request.data.keys():
        contextInstance.source = request.data['source']
      if 'origin' in request.data.keys():
        contextInstance.origin = request.data['origin']
      if 'categories' in request.data.keys():
        contextInstance.categories = request.data['categories']
      if (contextInstance.contentType.startswith("image/")):
          content = contextInstance.content
          if not content.startswith("data:image/"):
            url = content
            base64Img = base64.b64encode(requests.get(url).content).decode("utf-8")
            contextInstance.content = "data:" + contextInstance.contentType + "," + base64Img
      contextInstance.save()  
      postDataSerialized = json.loads(serializers.serialize('json', [contextInstance]))
      data = postDataSerialized[0]['fields']
      data['postID'] = postDataSerialized[0]['pID']
      data = postMethod.JSONFormatPost(request, data, authorID).data

      result = Response(status=201)
      result.data = data
      request.data.update(data)
      return result
    return Response(status=400)




  @staticmethod
  def PostByPostID(request, postID, authorID=None):
    try:
      data = postModel.Post.objects.filter(postURL__exact=postID)
      postVisibility = data[0].get_visible_authors().values()
      request.user.id = data[0].authorID.id
      postVisibility = list(postVisibility) 
      data = serializers.serialize('json', data)
      postID = json.loads(data)[0]['pID']
      data = json.loads(data)[0]['fields']
      data['postID'] = postID
    except:
      return Response(status=404)

    for i in range(len(postVisibility)):
      if str(postVisibility[i]['id']).split('/')[-1] == str(authorID):
        return Response(data)
    return Response(status=403)





  @staticmethod
  def getPostByAuthorID(request, authorID):
    try:
      value = postModel.Post.objects.filter(postAuthorID__exact=authorID)
      value = serializers.serialize('json', value)
      value = json.loads(value)
      value = sorted(value, key=lambda d: d['fields']["published"], reverse=True)
      for i in range(len(value)):
        value[i]['fields']['postID'] = value[i]['pID']
        value[i] = value[i]['fields']   
      return Response(value)
    except:
      return Response(status=404)

  @staticmethod
  def deletePostByPostId(request, authorID):
    url = request.build_absolute_uri()
    try:
      key = postModel.Post.objects.filter(postAuthorID__exact=authorID).filter(url__exact=url).delete()
      if key[0]:
        return Response(status=200)
      else:
        return Response(status=404)
    except:
      return Response(status=404)



  @staticmethod
  def postPagination(request, result, authorID, pageNumber, pageSize):
    data = result.data
    postPaginator = Paginator(data, pageSize)
    page = postPaginator.get_page(pageNumber)
    nextPage = ""
    previousPage = ""
    if page.has_next():
      nextPage = f"({request.build_absolute_uri(request.path)}?page={page.next_page_number()}&size={pageSize})"
    if page.has_previous():
      previousPage = f"({request.build_absolute_uri(request.path)}?page={page.previous_page_number()}&size={pageSize})"
    for i in range(len(page.object_list)):
      page.object_list[i] = postMethod.JSONFormatPost(request, page.object_list[i], authorID, page.object_list[i]['postID'], pageSize).data

    context = {
      'count': postPaginator.count,
      'posts': page.object_list,
      'next': nextPage,
      'prev': previousPage,
    }
    return Response(context)











  def JSONFormatPost(request, Post, authorID, postID = '', size=1):
    postID = Post['postID']
    User = None
    if Post.get('authorID', False):
      User = AuthorJSONID(Post['authorID']).data
    else:
      User = AuthorJSONID(authorID).data
    
    JSONResponsePost = {
      'author' : User,
      'type' : 'post',
      'title' : Post['title'],
      'id' : Post['url'],
      'description' : Post['description'],
      'contentType' : Post['contentType'],
      'content' : Post['content'],
      'published' : Post['published'],
      'visibility' : Post['visibility'],
      'unlisted' : Post['unlisted'],
    }
    if Post['source']:
      JSONResponsePost['source'] = Post['source']
    else:
      JSONResponsePost['source'] = Post['url']

    if Post['origin']:
      JSONResponsePost['origin'] = Post['origin']
    else:
      JSONResponsePost['origin'] = Post['url']

    if isinstance(Post["categories"], str):
        JSONResponsePost['categories'] = json.loads(Post['categories'])
    else:
        JSONResponsePost['categories'] = Post["categories"]

    if 'comments' in Post.keys():
      JSONResponsePost['count'] = 0
      JSONResponsePost['size'] = size
      JSONResponsePost['comment_url'] = Post['comment_url']
      JSONResponsePost['comments'] = Post['comments']
    else:
      result = postModel.Post.objects.filter(postID__exact=postID)
      if len(result) > 0:
        commentInfoResponse = commentMethod.postCommentInfo(result[0])
        JSONResponsePost['count'] = commentInfoResponse['count']
        JSONResponsePost['size'] = size
        JSONResponsePost['comment_url'] = commentInfoResponse['comment_url']
        JSONResponsePost['comments'] = commentInfoResponse['comments']
    return Response(JSONResponsePost)

  def VisiblePosts(request, authorID):
    try:
      totalVisiblePosts = []
      unlistedPosts = []
      posts = postModel.Post.objects.filter(unlisted__exact=False)
      postSerializedInfo = serializers.serialize('json', posts)
      postSerializedInfo = json.loads(postSerializedInfo)
      
      for eachPostVisibility in posts:
        if eachPostVisibility.visibility == "public":
            value = serializers.serialize('json', [eachPostVisibility, ])
            value = json.loads(value)[0]['fields']
            unlistedPosts.append(str(value['url']))
        else:
            authors = eachPostVisibility.get_visible_authors()
            request.user.id = eachPostVisibility.authorID.id

            if len(authors) > 0:
              list_of_authors = list(authors.values()) 
              for each_author in list_of_authors:
                  if str(each_author['id']).split('/')[-1] == str(authorID):
                      value = serializers.serialize('json', [eachPostVisibility, ])
                      value = json.loads(value)[0]['fields']
                      unlistedPosts.append(str(value['url']))

      for eachSeraializedInfo in range(len(postSerializedInfo)):
        postSerializedInfo[eachSeraializedInfo] = postSerializedInfo[eachSeraializedInfo]['fields']
        if postSerializedInfo[eachSeraializedInfo]['url'] in unlistedPosts:
          value = postModel.Post.objects.filter(url__exact=postSerializedInfo[eachSeraializedInfo]['url'])
          value = serializers.serialize('json', value)
          postId = json.loads(value)[0]['pID']
          postSerializedInfo[eachSeraializedInfo]['postID'] = postId
          totalVisiblePosts.append(postSerializedInfo[eachSeraializedInfo])

      return Response(totalVisiblePosts)
    except:
      return Response(status=404)
