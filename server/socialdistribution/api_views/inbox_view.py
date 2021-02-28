from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import *
from socialdistribution.serializers import *
import json

@api_view(['GET', 'POST', 'DELETE'])
def inbox_detail(request, authorID):
    if request.method == 'GET':
        # get everything in the inbox
        obj, created = Inbox.objects.get_or_create(authorID=authorID)
        serializer = InboxSerializer(obj)
        return Response(serializer.data)

    elif request.method == 'POST':
        content_type = request.data['type'] # post/follow/like

        if content_type == 'post':
            obj_id = request.data['obj_id']
            post = Post.objects.get(postID=obj_id)
            item_serializer = PostSerializer(post)

        elif content_type == 'follow':
            new_follower_ID = request.data['new_follower_ID']
            new_follower = get_object_or_404(Author, authorID=new_follower_ID)
            author = get_object_or_404(Author, authorID=authorID)
            # append to follow database if needed
            friend_object, created = Follow.objects.get_or_create(current_user=author)
            if new_follower not in friend_object.users.all():
                Follow.follow(author, new_follower)

            actor_name = new_follower.username
            object_name = author.username
            summary = actor_name + " wants to follow " + object_name
            new_follower_serialized = AuthorSerializer(new_follower).data
            author_serialized = AuthorSerializer(author).data

            item_serializer = author # init to avoid reference before assignment error
            item_serializer.data = {"type": "Follow","summary":summary,"actor":new_follower_serialized,"object":author_serialized}

        elif content_type == 'like':
            data = request.data
            like_sum = request.data['summary']
            data['author_write_article_ID'] = authorID
            if ("post" in like_sum):
                item_serializer = LikePostSerializer(data=data)
            elif("comment" in like_sum):
                item_serializer = LikeCommentSerializer(data=data)
            if item_serializer.is_valid():
                item_serializer.save() # save the item to the other form in db
            else:
                return Response({'message':item_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        inbox, _ = Inbox.objects.get_or_create(authorID=authorID)
        inbox.items.insert(0, item_serializer.data) # append to items list
        inbox.save()
        return Response({'message':'sent successfully!'}, status=status.HTTP_200_OK)
        #inbox_serializer = InboxSerializer(inbox)
        #new_data = inbox_serializer.data # make a copy of inbox
        #new_data['items'].insert(0, item_serializer.data) # append to items list

        # save new data
        # new_inbox_serializer = InboxSerializer(inbox, data=new_data,required=False)
        # if new_inbox_serializer.is_valid():
        #     new_inbox_serializer.save()
        #     return Response({'message':'sent successfully!'}, status=status.HTTP_200_OK)
        # return Response({'message':new_inbox_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        for x in Inbox.objects.all().iterator(): x.delete()
        return Response({'message':'inbox cleared'}, status=status.HTTP_200_OK)
