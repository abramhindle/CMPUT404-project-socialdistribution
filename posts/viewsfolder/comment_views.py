from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework import views, status
from rest_framework.response import Response

from posts.helpers import get_post, get_local_post, get_id_from_url
from posts.models import WWUser, Comment, Server
from posts.pagination import CustomPagination
from posts.serializers import CommentSerializer, PostSerializer


class CommentViewList(views.APIView):

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before posting
    def post(self, request, post_id):
        if not request.user.approved:
            raise PermissionDenied
        query = 'addComment'
        requestor_url = request.data.get('comment').get('author').get('url')
        requestor_id = get_id_from_url(requestor_url)
        WWUser.objects.get_or_create(url=requestor_url, user_id=requestor_id)
        post = get_local_post(post_id)
        # Post external send it off to another server
        if post is None:
            # TODO Allow commenting on nodes we aren't connected to
            data = request.data
            server_host = data.get('post').split('/post')[0]
            server = Server.objects.get(server=server_host)
            if server.send_external_comment(data):
                success = True
                message = "Comment Added"
                status_val = status.HTTP_200_OK
            else:
                success = False
                message = "Comment not allowed"
                status_val = status.HTTP_403_FORBIDDEN
        else:
            # Post is local
            ww_user = WWUser.objects.get_or_create(url=requestor_url, user_id=requestor_id)[0]
            serializer = CommentSerializer(data=request.data['comment'], context={'post_id': post_id, 'user': ww_user})
            if serializer.is_valid():
                serializer.save()
                success = True
                message = "Comment Added"
                status_val = status.HTTP_200_OK
            else:
                success = False
                message = "Comment not allowed"
                status_val = status.HTTP_403_FORBIDDEN

        data = {'message': message, 'success': success, 'query': query}
        return Response(data=data, status=status_val)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, post_id):
        paginator = CustomPagination()
        comments = Comment.objects.filter(parent_post_id=post_id).order_by("-published")
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, "comments")


class FrontEndCommentView(TemplateView):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request, post_id):
        if not request.user.approved:
            raise PermissionDenied
        post = get_post(post_id)
        serializer = PostSerializer(post)
        return render(request, 'post/post.html',
                      context={'post': serializer.data, 'comments': serializer.data["comments"]})
