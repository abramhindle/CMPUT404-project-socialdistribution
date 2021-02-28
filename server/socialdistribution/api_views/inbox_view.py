from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import *
from socialdistribution.serializers import *

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

        

