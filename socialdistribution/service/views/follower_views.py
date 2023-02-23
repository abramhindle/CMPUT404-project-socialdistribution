# from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, \
#     RetrieveAPIView, RetrieveDestroyAPIView


# # TODO all below are just scatch and need to be fixed and rebuilt 

# class FollowersAPIView(RetrieveAPIView):
#     """ GET an Author's all followers """

#     # serializer_class = serializers.FollowersSerializer
#     # renderer_classes = (renderers.FollowersRenderer,)
#     http_method_names = ['get']

#     def retrieve(self, request, *args, **kwargs):
#         queryset = []
#         uuid = self.kwargs['author']
#         author = Author.objects.filter(uuid=uuid).first()
#         followers = FollowerCount.objects.filter(user=author.username)
#         for follower in followers:
#             author = model_to_dict(Author.objects.filter(username=follower.follower).first())
#             serializer = serializers.AuthorSerializer(author)
#             queryset.append(serializer.data)
#         response = {"type": "followers", "items": queryset}
#         return Response(response)

# class FollowerAPIView(RetrieveUpdateDestroyAPIView):
#     """ GET if is a follower PUT a new follower DELETE an existing follower"""

#     serializer_class = serializers.FollowersSerializer
#     renderer_classes = [JSONRenderer]
#     # TODO foreign author (currently our author)

#     def usernames(self, *args, **kwargs):
#         follower_uuid = self.kwargs['another_author']
#         follower = Author.objects.filter(uuid=follower_uuid).first()
#         user_uuid = self.kwargs['author']
#         user = Author.objects.filter(uuid=user_uuid).first()
#         return follower.username, user.username

#     def relation_check(self, *args, **kwargs):
#         usernames = self.usernames()
#         followers = FollowerCount.objects.filter(user=usernames[1]).values_list('follower', flat=True)
#         if usernames[0] in followers:
#             return True
#         return False

#     def retrieve(self, request, *args, **kwargs):

#         if self.relation_check():
#             return Response({'following_relation_exist': 'True'})
#         else:
#             return Response({'following_relation_exist': 'False'})

#     def put(self, request, *args, **kwargs):
#         if self.relation_check():
#             return Response({'following_relation_exist': 'True',
#                              'following_relation_put': 'False'})
#         else:
#             try:
#                 usernames = self.usernames()
#                 FollowerCount.objects.create(follower=usernames[0], user=usernames[1])
#                 return Response({'following_relation_exist': 'False',
#                                  'following_relation_put': 'True'})
#             except:
#                 return Response({'following_relation_exist': 'False',
#                                  'following_relation_put': 'False'})

#     def delete(self, request, *args, **kwargs):
#         if self.relation_check():
#             usernames = self.usernames()
#             relation = FollowerCount.objects.filter(follower=usernames[0]).filter(user=usernames[1])
#             try:
#                 relation.delete()
#                 return Response({'following_relation_exist': 'True',
#                                  'following_relation_delete': 'True'})
#             except:
#                 return Response({'following_relation_exist': 'True',
#                                  'following_relation_delete': 'False'})
#         else:
#             return Response({'following_relation_exist': 'False',
#                                  'following_relation_delete': 'False'})

