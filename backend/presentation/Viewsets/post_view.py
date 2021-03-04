from presentation.models import Author, Follower, Post, Comment, Inbox
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from presentation.Serializers.post_serializer import PostSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse

'''
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
GET get the public post
POST update the post (must be authenticated)
DELETE remove the post
PUT create a post with that post_id

Creation URL ://service/author/{AUTHOR_ID}/posts/
GET get recent posts of author (paginated)
POST create a new post but generate a post_id

Be aware that Posts can be images that need base64 decoding.
posts can also hyperlink to images that are public
'''


def getAuthorIDFromRequestURL(request, id):
    parsed_url = urlparse(request.build_absolute_uri())
    host = '{url.scheme}://{url.hostname}:{url.port}'.format(
        url=parsed_url)
    author_id = f"{host}/author/{id}"
    return author_id


def getPostIDFromRequestURL(request, id):
    post_id = f"/posts/{id}"
    return post_id


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    # GET a list of posts
    # URL: ://service/author/{AUTHOR_ID}/posts/
    def list(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = get_object_or_404(Author, id=author_id)
        queryset = Post.objects.filter(author=author)
        if queryset.exists():
            posts = Post.objects.filter(author=author)
            posts = list(posts.values())
            # May have mistakes here, do we need to change comment model?
            return JsonResponse(posts, safe=False)
        else:
            Post.objects.create(author=author)
            return Response({
                'type': 'post',
                'items': []
            })

    # GET a single post using post_id
    # URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}

    def retrieve(self, request, *args, **kwargs):
        post_id = request.build_absolute_uri()
        queryset = Post.objects.get(id=post_id)
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

    # POST on an existing post
    # URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        #post_id = request_data.get('id', None)
        post_id = request.build_absolute_uri()
        post = Post.objects.get(id=post_id)
        new_title = request_data.get('title', None)
        new_source = request_data.get('source', None)
        new_origin = request_data.get('origin', None)
        new_description = request_data.get('description', None)
        new_contentType = request_data.get('contentType', None)
        new_content = request_data.get('content', None)
        new_categories = request_data.get('categories', None)
        new_count = request_data.get('count', None)
        new_size = request_data.get('size', None)
        if new_title:
            post.title = new_title
        if new_source:
            post.source = new_source
        if new_origin:
            post.origin = new_origin
        if new_description:
            post.description = new_description
        # if new_contentType:
        #    post.contentType = new_contentType
        if new_content:
            post.content = new_content
        if new_categories:
            post.categories = new_categories
        if new_count:
            post.count = new_count
        if new_size:
            post.size = new_size
        post.save()
        return Response("Post updated successfully", 204)

    # PUT create a post with that post_id
    # URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
    def build(self, request, *args, **kwargs):
        request_data = request.data.copy()
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        author = get_object_or_404(Author, id=author_id)
        title = request_data.get('title', None)
        source = request_data.get('source', None)
        origin = request_data.get('origin', None)
        description = request_data.get('description', None)
        contentType = request_data.get('contentType', None)
        content = request_data.get('content', None)
        categories = request_data.get('categories', None)
        count = request_data.get('count', None)
        size = request_data.get('size', None)
        comments = request_data.get('comments', None)
        visibility = request_data.get('visibility',None)
        unlisted = request_data.get('unlisted', False)
        post_data = {'title': title, 'id': post_id, 'source': source,
                    'origin': origin, 'description': description, 'contentType': contentType,
                    'content': content, 'author': author_id, 'categories': categories,
                    'count': count, 'size': size, 'comments': comments,
                    'visibility': visibility, 'unlisted': unlisted}

        # send to followers' inboxes
        queryset = Follower.objects.filter(owner=author)
        if queryset.exists():
            followers = Follower.objects.get(owner=author)
            for follower_id in followers.items:
                follower = Author.objects.get(id=follower_id)
                inbox = Inbox.objects.get(author=follower)
                inbox.items.append(post_data)
                inbox.save()
        serializer = self.serializer_class(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 200)

    # POST create a new post
    # URL: ://service/author/{AUTHOR_ID}/posts/
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = Author.objects.get(id=author_id)
        title = request_data.get('title', None)
        source = request_data.get('source', None)
        origin = request_data.get('origin', None)
        description = request_data.get('description', None)
        contentType = request_data.get('contentType', None)
        content = request_data.get('content', None)
        categories = request_data.get('categories', None)
        count = request_data.get('count', None)
        size = request_data.get('size', None)
        #comments = request_data.get('comments', None)
        visibility = request_data.get('visibility',None)
        unlisted = request_data.get('unlisted', False)

        # create post id
        puuid = str(uuid.uuid4().hex)
        post_id = f"{author_id}/posts/{puuid}"
        comments = f"{post_id}/comments/"
        post_data = {'title': title, 'id': post_id, 'source': source,
                    'origin': origin, 'description': description, 'contentType': contentType,
                    'content': content, 'author': author_id, 'categories': categories,
                    'count': count, 'size': size, 'comments': comments,
                    'visibility': visibility, 'unlisted': unlisted}

        # send to followers' inboxes
        queryset = Follower.objects.filter(owner=author)
        if queryset.exists():
            followers = Follower.objects.get(owner=author)
            for follower_id in followers.items:
                follower = Author.objects.get(id=follower_id)
                inbox = Inbox.objects.get(author=follower)
                inbox.items.append(post_data)
                inbox.save()

        serializer = self.serializer_class(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        else:
            return Response(serializer.errors,
                            status=400)

    # DELETE a single post using post_id
    # URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
    def delete(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        post = get_object_or_404(Post, id=post_id)
        # Possible mistake?
        try:
            post.delete()
        except ValueError:
            return Response("No such a post. Deletion fails.", 500)
        return Response("Delete successful")
