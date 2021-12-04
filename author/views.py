import json
from functools import partial
import requests
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.core.validators import URLValidator
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from post.models import Like
from post.serializers import LikeSerializer
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author import serializers

from .models import Author, Follow, Inbox
from post.models import Post, Like, Comment
from server.models import Setting, Node
from .serializers import AuthorSerializer
from post.serializers import LikeSerializer, CommentSerializer, PostSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Social_Distribution import utils


class index(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        GET: retrieve all profiles on the server paginated. Does not return authors from other nodes.
            * If no page and size are given, returns all authors instead
            * If invalid parameters are given e.g. size = 0, negative page number, sends 400 Bad Request
        '''
        utils.update_authors()
        author_query = Author.objects.filter(node=None).order_by("authorID")
        param_page = request.GET.get("page", None)
        param_size = request.GET.get("size", None)
        if param_page != None and param_size != None:
            authorPaginator = Paginator(author_query, param_size)
            authors_data = []
            try:
                authors_data = AuthorSerializer(authorPaginator.page(param_page), many=True).data
            except (PageNotAnInteger, ZeroDivisionError):
                # bad request where page is not a number
                return Response(status=400)
            except EmptyPage:
                pass

            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)
        else:
            # return all authors
            authors_data = AuthorSerializer(author_query, many=True).data
            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)

class allAuthors(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        GET: retrieve all profiles on the server paginated
            * If no page and size are given, returns all authors instead
            * If invalid parameters are given e.g. size = 0, negative page number, sends 400 Bad Request
        '''
        utils.update_authors()
        author_query = Author.objects.all().order_by("authorID")
        param_page = request.GET.get("page", None)
        param_size = request.GET.get("size", None)
        if param_page != None and param_size != None:
            authorPaginator = Paginator(author_query, param_size)
            authors_data = []
            try:
                authors_data = AuthorSerializer(authorPaginator.page(param_page), many=True).data
            except (PageNotAnInteger, ZeroDivisionError):
                # bad request where page is not a number
                return Response(status=400)
            except EmptyPage:
                pass

            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)
        else:
            # return all authors
            authors_data = AuthorSerializer(author_query, many=True).data
            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)


class profile(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, author_id):
        try:
            author_profile = Author.objects.get(authorID=author_id)
            serializer = AuthorSerializer(author_profile)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response("This author does not exist", status=404)

    def post(self, request, author_id):
        if request.user.is_authenticated:
            try:
                user_author = request.user.author
            except:
                return Response("The user does not have an author profile.", status=401)
            if str(user_author.authorID) != author_id:
                return Response("The user does not have permission to modify this profile.", status=401)

            try:
                author = Author.objects.get(authorID=author_id)
                update_data = request.data
                serializer = AuthorSerializer(author, data=update_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                else:
                    print(serializer.errors)
                return Response(status=422)
            except Author.DoesNotExist:
                return Response(status=404)
        return Response("The user is not authenticated.", status=401)

class login(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response("Missing username or password.", status=400)
        if username is None or password is None:
            return Response("Bad request. The expected keys 'username' and 'password' were not found.", status=400)
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            try:
                author_serializer = AuthorSerializer(user.author)
            except Author.DoesNotExist:
                return Response("The user credentials are not associated with an author.", status=400)
            django_login(request, user)
            return Response(author_serializer.data, status=200)
        else:
            return Response("Invalid login credentials.", status=401)


class logout(APIView):
    def post(self, request):
        django_logout(request)
        return Response(status=200)


class register(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response("Bad request. The expected keys 'username' and 'password' were not found.", status=400)
        if User.objects.filter(username=username).exists():
            # The user already exists
            return Response("The given username is already in use.", status=409)
        user = User.objects.create_user(username=username, password=password)
        if Setting.user_sign_up_enabled():
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        author = Author(user=user, host=request.build_absolute_uri('/'), displayName=username, node=None)
        author.save()
        return Response("A new user was created.", status=201)


class followers(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        utils.update_authors()
        try:
            author = Author.objects.get(authorID=author_id)
        except:
            # The author does not exist
            return Response(status=404)
        follower_ids = Follow.objects.filter(toAuthor=author_id)
        follower_profiles = Author.objects.filter(authorID__in=follower_ids.values_list('fromAuthor', flat=True))
        serializer = AuthorSerializer(follower_profiles, many=True)
        response = {'type': 'followers', 'items': serializer.data}
        return Response(response)


class follower(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, foreign_author_id):
        try:
            author = Author.objects.get(authorID=author_id)
        except Author.DoesNotExist:
            # The author does not exist
            return Response(status=404)
        try:
            validate = URLValidator()
            validate(foreign_author_id)
            foreignID = foreign_author_id.split("/")[-1]
        except ValidationError as e:
            foreignID = foreign_author_id
        if author.node is not None:
            print(foreignID)
            follower = Author.objects.get(authorID=foreignID)
            if author.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/": 
                response = requests.get(author.node.host_url + "author/" + str(author.authorID) + "/followers/" + follower.get_url(), auth=(author.node.username, author.node.password))
                print(author.node.host_url + "author/" + str(author.authorID) + "/followers/" + follower.get_url())
            else:
                response = requests.get(author.node.host_url + "author/" + str(author.authorID) + "/followers/" + foreign_author_id + "/", auth=(author.node.username, author.node.password))
                print(author.node.host_url + "author/" + str(author.authorID) + "/followers/" + foreign_author_id + "/")
            if response.status_code >= 300:
                return Response(response.text, response.status_code)
            if response.text == '"true"':
                serializer = AuthorSerializer(follower)
                return Response(serializer.data, status=200)
            elif response.text == '"false"':
                return Response(status=404)
            return Response(response.json(), response.status_code)
        else:
            follow = Follow.objects.filter(toAuthor=author_id, fromAuthor=foreignID)
            if not follow:
                return Response(status=404)
            else:
                follower = Author.objects.get(authorID=foreignID)
                serializer = AuthorSerializer(follower)
                return Response(serializer.data, status=200)

    def put(self, request, author_id, foreign_author_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response(status=403)

            # Update the authors on the local node in case the author being put is on a different node
            utils.update_authors()

            try:
                fromAuthor = Author.objects.get(authorID=foreign_author_id)
            except:
                return Response(status=404)

            if Follow.objects.filter(fromAuthor=fromAuthor, toAuthor=author).exists():
                # The follower already exists
                return Response(status=409)
            # Add the follower
            follow = Follow.objects.create(fromAuthor=fromAuthor, toAuthor=author, date=timezone.now())
            follow.save()
            return Response(status=201)
        else:
            # Request was not authenticated
            return Response(status=401)

    def delete(self, request, author_id, foreign_author_id):
        try:
            author = request.user.author
        except:
            # The user does not have an author profile
            return Response(status=403)
        if str(author.authorID) != author_id:
            # The request was made by a different author
            return Response(status=403)
        try:
            Follow.objects.get(fromAuthor=foreign_author_id, toAuthor=author_id).delete()
        except:
            # Nothing to delete
            return Response(status=404)
        return Response(status=200)

class liked(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        if not Author.objects.filter(authorID=author_id).exists():
            return Response(status=404)
        liked = Like.objects.filter(fromAuthor=author_id)
        serializer = LikeSerializer(liked, many=True)
        response = {"type": "liked", "items": serializer.data}
        return Response(response, status=200)

class inbox(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        # Return 404 if the inbox does not exist
        if not Author.objects.filter(authorID=author_id).exists():
            return Response("The requested author does not exist.", status=404)

        # Return 403 if somebody other than the author requests their inbox
        try:
            author = request.user.author
        except Author.DoesNotExist:
            return Response("You do not have permission to fetch this inbox.", status=403)
        if str(author.authorID) != author_id:
            return Response("You do not have permission to fetch this inbox.", status=403)
        
        # Return the inbox contents
        response = {"type": "inbox", "author": request.user.author.get_url(), "items": []}
        author_inbox = Inbox.objects.filter(authorID = author_id).order_by("-date")
        try:
            size = int(request.query_params.get("size", 5))
            page = int(request.query_params.get("page", 1))
            paginator = Paginator(author_inbox, size)
            inbox_page = paginator.get_page(page)
        except:
            return Response("Bad request. Invalid size or page parameters.", status=400)
        for item in inbox_page:
            if item.inboxType.lower() == "post":
                try:
                    post = Post.objects.get(postID=item.objectID)
                except:
                    continue
                serializer = PostSerializer(post)
                response["items"].append(serializer.data)
            elif item.inboxType.lower() == "follow":
                actor_serializer = AuthorSerializer(item.fromAuthor)
                object_serializer = AuthorSerializer(request.user.author)
                item = {"type": "Follow", "summary": item.summary, "actor": actor_serializer.data, "object": object_serializer.data}
                response["items"].append(item)
            elif item.inboxType.lower() == "like":
                try:
                    like = Like.objects.get(authorID=item.fromAuthor, objectID=item.objectID)
                except:
                    continue
                serializer = LikeSerializer(like)
                response["items"].append(serializer.data)
            elif item.inboxType.lower() == "comment":
                try:
                    comment = Comment.objects.get(commentID=item.objectID)
                except:
                    continue
                serializer = CommentSerializer(comment)
                response["items"].append(serializer.data)
        return Response(response, status=200)

    def post(self, request, author_id):
        print(request.data)
        # Update authors in case this was sent by or to an author that our local node does not know about
        utils.update_authors()

        # return 404 if the author does not exist
        try:
            inbox_recipient = Author.objects.get(authorID=author_id)
        except Author.DoesNotExist:
            return Response("The author specified in the url does not exist.", status=404)

        if inbox_recipient.node is not None:
            # send the data to the correct host
            try:
                if inbox_recipient.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                    destination = inbox_recipient.node.host_url + "author/" + author_id + "/inbox"
                else:
                    destination = inbox_recipient.node.host_url + "author/" + author_id + "/inbox/"
                response = requests.post(destination, auth=(inbox_recipient.node.username, inbox_recipient.node.password), json=request.data)
                if response.status_code >= 300:
                    print("Could not connect to the host: " + inbox_recipient.host)
                    print(response.text)
                    print(response.status_code)
                    print(destination)
                    print(request.data)
                else:
                    print("Sent to inbox!")
                    print(response.status_code)
            except Exception as e:
                print(e)
                return Response("Could not connect to the host: " + inbox_recipient.host, status=400)
            return Response(response.text, status=response.status_code)
            
        data = request.data
        try:
            if data["type"].lower() == "post":
                # save the post to the Post table if it is not already there
                print(data)
                if data["id"] != None:
                    postID = data["id"].split("/")[-1]
                else: 
                    postID = None
                postAuthorID = data["author"]["id"].split("/")[-1]
                try:
                    fromAuthor = Author.objects.get(authorID=postAuthorID)
                except Author.DoesNotExist:
                    return Response("The author with id " + postAuthorID  + " was expected to be on the server but was not found.", status=400)
                if postID == None or not Post.objects.filter(postID=postID).exists():
                    print("creating post...")
                    serializer = PostSerializer(data=data)
                    if serializer.is_valid():
                        post = serializer.save()
                        postID = post.postID
                        print(post)
                    else:
                        print(serializer.errors)
                        return Response(status=400)
                # save the post to the inbox
                inboxType = data["type"]
                date = datetime.now(timezone.utc).astimezone().isoformat()
                content_type = ContentType.objects.get(model="post")
                Inbox.objects.create(authorID=inbox_recipient, inboxType=inboxType, date=date, objectID=postID, fromAuthor=fromAuthor, content_type=content_type)
            elif data["type"].lower() == "follow":
                # save the follow to the inbox
                inboxType = data["type"]
                summary = data["summary"]
                fromAuthorID = data["actor"]["id"].split("/")[-1]
                try:
                    fromAuthor = Author.objects.get(authorID=fromAuthorID)
                except Author.DoesNotExist:
                    return Response("The author with id " + fromAuthorID  + " was expected to be on the server but was not found.", status=400)
                date = timezone.now()
                Inbox.objects.create(authorID=inbox_recipient, inboxType=inboxType, summary=summary, fromAuthor=fromAuthor, date=date)
            elif data["type"].lower() == "like":
                objectID = data["object"].split("/")[-1]
                fromAuthorID = data["author"]["id"].split("/")[-1]
                try:
                    fromAuthor = Author.objects.get(authorID=fromAuthorID)
                except Author.DoesNotExist:
                    return Response("The author with id " + fromAuthorID  + " was expected to be on the server but was not found.", status=400)
                # return a 409 response if the like already exists
                if Like.objects.filter(objectID=objectID, authorID=fromAuthorID).exists():
                    return Response("The object has already been liked by this author.", status=409)
                # Save the like to the Like table
                serializer = LikeSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response("Bad Request. Data could not be validated.", status=400)
                # Save the like to the inbox
                inboxType = data["type"]
                summary = data["summary"]
                # context = data["@context"]
                date = timezone.now()
                if "/comments" in data["object"]:
                    content_type = ContentType.objects.get(model="comment")
                else:
                    content_type = ContentType.objects.get(model="post")
                Inbox.objects.create(authorID=inbox_recipient, inboxType=inboxType, summary=summary, fromAuthor=fromAuthor, date=date, objectID=objectID, content_type=content_type)
            elif data["type"].lower() == "comment":
                print(data)
                if "id" in data:
                    if "/comments" in data["id"]:
                        commentID = data["id"].split("/")[-1]
                        # Save comment to comment table if it does not already exist
                        if not Comment.objects.filter(commentID=commentID).exists():
                            postID = data["id"].split("/")[-3]
                            serializer = CommentSerializer(data=data, context = {"post_id": postID})
                            if serializer.is_valid():
                                comment = serializer.save()
                            else:
                                print(serializer.errors)
                                return Response(status=400)
                    else:
                        postID = data["id"].split("/")[-1]
                        serializer = CommentSerializer(data=data, context = {"post_id": postID})
                        if serializer.is_valid():
                            comment = serializer.save()
                        else:
                            print(serializer.errors)
                            return Response(status=400)
                elif "object" in data:
                    postID = data["object"].split("/")[-1]
                    serializer = CommentSerializer(data=data, context = {"post_id": postID})
                    if serializer.is_valid():
                        comment = serializer.save()
                    else:
                        print(serializer.errors)
                        return Response(status=400)
                else:
                    return Response(status=400)
                # save the comment to the inbox
                inboxType = data["type"]
                fromAuthorID = data["author"]["id"].split("/")[-1]
                try:
                    fromAuthor = Author.objects.get(authorID=fromAuthorID)
                except Author.DoesNotExist:
                    return Response("The author with id " + fromAuthorID  + " was expected to be on the server but was not found.", status=400)
                date = comment.date
                objectID = comment.commentID
                content_type = ContentType.objects.get(model="comment")
                Inbox.objects.create(authorID=inbox_recipient, inboxType=inboxType, fromAuthor=fromAuthor, date=date, objectID=objectID, content_type=content_type)
            else:
                return Response("Bad Request. Type was not post, like, comment, or follow.", status=400)
        except KeyError as e:
            return Response("Bad Request. KeyError.", status=400)
        return Response(status=201)

    def delete(self, request, author_id):
        # Return 404 if the inbox does not exist
        if not Author.objects.filter(authorID=author_id).exists():
            return Response("The requested author does not exist.", status=404)

        # Return 403 if somebody other than the author tries to delete the inbox
        try:
            author = request.user.author
        except Author.DoesNotExist:
            print("User has no author")
            return Response("You do not have permission to clear this inbox.", status=403)
        if str(author.authorID) != author_id:
            print("User is not inbox owner")
            return Response("You do not have permission to clear this inbox.", status=403)

        Inbox.objects.filter(authorID = author_id).delete()
        return Response(status=200)
