from rest_framework.decorators import api_view
from rest_framework.response import Response
from .authorView import AuthorJSONID
from ..models.commentModel import Comment
from ..models.authorModel import Author
from ..models.postModel import Post
from ..serializers import CommentSerializer
from django.core import serializers
import json

from django.core.paginator import Paginator

@api_view(['GET'])
def CommentList(request, commentAuthorID, commentPostID):
    # List all the followers
    if request.method == 'GET':
        try:
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/#limiting-querysets
            comments = Comment.objects.filter(author=commentAuthorID, post=commentPostID)
            post = Comment.objects.filter(author=commentAuthorID, post=commentPostID)[0].post.id
        except:
            return Response(status=404)
        serializer = CommentSerializer(comments, many=True)
        new_data = {'type': 'comments', 'post': post, 'id': post + 'comments' }
        new_data.update({
            'comments': serializer.data,
        })
        return Response(new_data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def CommentDetail(request, commentAuthorID, commentPostID, commentID):
  
  if request.method == 'GET':
    try:
      comment = Comment.objects.get(author=commentAuthorID, post=commentPostID, id=commentID)
    except:
        return Response(status=404)
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data, status=200)

  elif request.method == 'PUT':
    comment = Comment.objects.get(author=commentAuthorID, post=commentPostID, id=commentID)
    serializer = CommentSerializer(instance=comment, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Comment updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=400)

  elif request.method == 'DELETE':
    comment = Comment.objects.get(author=commentAuthorID, post=commentPostID, id=commentID)
    comment.delete()

    return Response({"status": 0, "message": "Comment deleted"}, status=204)
  else:
    return Response(status=405)
    
# Creates a comment on post
class commentMethod:
    @staticmethod
    def createPostComment(request, authorID, postID):
        try:
            postObject = Post.objects.filter(postURL__exact=postID)
            authorObject = Author.objects.filter(aID=request.user.id)
            if not postObject.exists(): return Response("Post does not exist" , status=400)

            authorizedAuthors = postObject[0].get_visible_authors(get_friends=True)
            if authorObject[0] not in authorizedAuthors: return Response("Unauthorized User", status=403)

            commentSerializer = CommentSerializer(data=request.data,
                context={'request': request, 'postID': postObject[0]})
            if not commentSerializer.is_valid():
                return Response("Invalid data provided", status=400)
            
            createnewComment = json.loads(serializers.serialize('json',[commentSerializer.save()]))[0]['fields']
            return Response(commentMethod.commentFormatJSON(request, createnewComment), status=201)
        except Exception as e:
            print(e)
            return Response(status=400)

    # Obtains comments for a post
    @staticmethod
    def getPostComments(request, authorID, postID):
        try:
            postObject = Post.objects.filter(postURL__exact=postID)
            authorObject = Author.objects.filter(aID=request.user.id)
            if not postObject.exists(): return Response("Post does not exist" , status=400)

            authorizedAuthors = postObject[0].get_visible_authors(get_friends=True)
            if authorObject[0] not in authorizedAuthors: return Response("Author does not exist", status=403)

            allComments = Comment.objects.filter(commentPostID__exact=postObject[0].postID).order_by("-published")
            
            pageSize = request.GET.get('size', 5)
            pageNum = request.GET.get('page', 1)
            result = commentMethod.getPaginatedComments(request, allComments, pageSize,pageNum)
            return Response(result, status=200)   
        except Exception as e:
            print(e)
            return Response(status=400)
    
    # obtains comment for a given post
    @staticmethod
    def postCommentInfo(post):
        commentObject = Comment.objects.filter(commentPostID__exact=post.postID).order_by("-published")[:5]
        commentObject = json.loads(serializers.serialize('json', commentObject))
        for i in range(len(commentObject)):
            commentObject[i] = commentMethod.commentFormatJSON(None, commentObject[i]['fields'])
        commentDetails = {
            'comment_url' : f'{post.url}/comments',
            'count' : Comment.objects.filter(commentPostID__exact=post.postID).count(),
            'comments' : commentObject,
        }
        return commentDetails

    # Jsonformatter
    @staticmethod
    def commentFormatJSON(request, comment):
        JSONcomment = {
            'type' : "comment",
            'author' : AuthorJSONID(comment['Comment_authorID']).data,
            "comment" : comment["content"],
            "contentType" : comment["contentType"],
            "published" : comment["published"],
            "id" : comment["url"],
        }
        return JSONcomment

    # Comment Paginatier 
    @staticmethod
    def commentsPaginator(request,comments, size, num):
        commentPaginater = Paginator(comments, size)
        page = commentPaginater.get_page(num)
        prevPage = ""
        nextPage = ""
        if page.has_next():
            nextPage = f"({request.build_absolute_uri(request.path)}?page={page.next_page_number()}&size={size})"
        if page.has_previous():
            prevPage = f"({request.build_absolute_uri(request.path)}?page={page.previous_page_number()}&size={size})"

        page.object_list = json.loads(serializers.serialize('json', page.object_list))
        for i in range(len(page.object_list)):
            page.object_list[i] = commentMethod.commentFormatJSON(request, page.object_list[i]['fields'])

        context = {
            'count': commentPaginater.count,
            'comments': page.object_list,
            'next': nextPage,
            'prev': prevPage,
        }

        return context