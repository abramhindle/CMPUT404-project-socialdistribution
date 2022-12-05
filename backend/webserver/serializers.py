from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from .models import Author, Follow, FollowRequest, Inbox, Post, Node, Like, RemoteAuthor, RemotePost, Comment
from .api_client import http_request
from .utils import join_urls, format_uuid_without_dashes

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'display_name', 'profile_image', 'github_handle']


class RemoteAuthorSerializer(serializers.Serializer):
    class Meta:
        model = RemoteAuthor
    
    def to_representation(self, instance):
        node = instance.node
        res, _ = http_request("GET", instance.get_absolute_url(), expected_status=200, node=node)
        if res is None:
            return None
        return node.get_converter().convert_author(res)


class RemotePostSerializer(serializers.Serializer):
    class Meta:
        model = RemotePost
    
    def to_representation(self, instance):
        node = instance.author.node
        # e.g. http://127.0.0.1:5454/authors/241/posts/123
        # assumes that this route will return ALL posts for the author no matter it's visibility
        # TODO: confirm this assumption when connecting with other groups
        url = join_urls(instance.author.get_absolute_url(), "posts")
        res, _ = http_request("GET", url, expected_status=200, node=node)
        if res is None:
            return None
        converted_posts = node.get_converter().convert_posts(res)
        for post in converted_posts:
            if node.team == 11:
                if (format_uuid_without_dashes(instance.id) in post.get("id", "")):
                    return post
            else:
                if str(instance.id) in post.get("id", ""):
                    return post
        return None


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    count = serializers.SerializerMethodField('count_comments')
    likes_count = serializers.SerializerMethodField('count_likes')
    comments = serializers.SerializerMethodField('get_comments_url')

    class Meta:
        model = Post
        fields = ['id','author','created_at','edited_at','title','description','source','origin',
                  'unlisted','content_type','content','visibility','likes_count','count','comments']
    
    def count_likes(self, post):
        # return Like.objects.filter(post=post.id).count()
        return post.like_set.count()

    def count_comments(self, post):
        return post.comment_set.count()
    
    def get_comments_url(self, post):
        # useless field to meet the "spec"
        return join_urls(post.get_url(self.context.get("request", None)), "comments")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "image" in data["content_type"]:
            data["content"] = data["content"].strip("b'").strip("'")

        if instance.visibility == "PUBLIC" or self.context.get("request", None).user.id == instance.author.id:
            comments_queryset = instance.comment_set.order_by("-created_at").all()[:5]
            data["comments_src"] = {
                "type": "comments",     # useless field to meet the "spec"
                "page": 1,              # useless field to meet the "spec"
                "size": comments_queryset.count(),
                "comments": CommentSerializer(comments_queryset, many=True, context=self.context).data
            }
        return data

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','description','unlisted','content']



class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','description','unlisted','content','visibility',"content_type"]


class CreateImagePostSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=Post.IMAGE_TYPE_CHOICES)
    image = Base64ImageField()
    # making image posts unlisted by default so that they don't show up on timelines
    unlisted = serializers.BooleanField(default=True, required=False)
    # making images public by default so that are publicly accessible by a url
    visibility = serializers.ChoiceField(choices=Post.VISIBILITY_CHOICES, default="PUBLIC", required=False)

    class Meta:
        model = Post
        fields = ['content_type', 'image', 'unlisted', 'visibility']


class AuthorRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Author
        fields = ['username', 'display_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        author = Author(username=self.validated_data['username'], display_name=self.validated_data['display_name'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        author.set_password(password)
        author.save()
        return author


class ActorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    url = serializers.URLField()


class SendFollowRequestSerializer(serializers.Serializer):
    sender = ActorSerializer()
    receiver = ActorSerializer()

class PostActorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    author = ActorSerializer()

class SendPrivatePostSerializer(serializers.Serializer):
    receiver = ActorSerializer()


class SendPostInboxSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    author = ActorSerializer()

class SendLikeSerializer(serializers.Serializer):
    author = ActorSerializer()
    post = PostActorSerializer(required=False)
    comment_url = serializers.URLField(required=False)


class SendCommentInboxSerializer(serializers.Serializer):
    author = ActorSerializer()
    post = PostActorSerializer()
    comment = serializers.CharField()
    content_type = serializers.ChoiceField(choices=Comment.CONTENT_TYPE_CHOICES, default="text/plain", required=False)


class FollowRequestSerializer(serializers.ModelSerializer):
    sender = AuthorSerializer(read_only=True)
    remote_sender = RemoteAuthorSerializer(read_only=True)

    class Meta:
        model = FollowRequest
        fields = ['sender', 'remote_sender']

    # reduces one layer of nesting i.e. removes the 'sender' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowRequestSerializer, self).to_representation(instance)
        if instance.remote_sender:
            data['sender'] = data['remote_sender']
        return data['sender']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    remote_author = RemoteAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'remote_author', 'comment', 'content_type', 'created_at', 'id']
    
    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        if instance.remote_author:
            data['author'] = data['remote_author']
        data.pop('remote_author', None)
        data['id'] = instance.get_url(self.context.get('request', None))
        return data


class LikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    remote_author = RemoteAuthorSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['author', 'remote_author', 'post', 'comment']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.post:
            # Mark: I am doing this so that I can display the post like this 
            # "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            data['post'] = join_urls(data['author']['url'], "posts", str(data['post']), ends_with_slash=True)
            data['object'] = data['post']
            data.pop('comment', None)
        else:
            data['comment'] = instance.comment.get_url(self.context.get('request', None))
            data['object'] = data['comment']
            data.pop('post', None)

        if instance.remote_author:
            data['author'] = data['remote_author']
        data.pop('remote_author', None)
        return data

class AcceptOrDeclineFollowRequestSerializer(serializers.Serializer):
    follow_request_sender = ActorSerializer()


class RemoveFollowerSerializer(serializers.Serializer):
    follower = ActorSerializer()


class FollowerSerializer(serializers.ModelSerializer):
    follower = AuthorSerializer(read_only=True)
    remote_follower = RemoteAuthorSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'remote_follower']

    # reduces one layer of nesting i.e. removes the 'follower' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowerSerializer, self).to_representation(instance)
        if instance.remote_follower:
            data['follower'] = data['remote_follower']
        return data['follower']


class InboxFollowRequestSerializer(FollowRequestSerializer):
    # adds the 'sender' field back into the representation
    def to_representation(self, instance):
        data = super(InboxFollowRequestSerializer, self).to_representation(instance)
        return {"sender": data}


class InboxSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    follow_request_received = InboxFollowRequestSerializer(read_only=True)
    remote_post = RemotePostSerializer(read_only=True)
    like = LikeSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Inbox
        fields = ['post', 'follow_request_received', 'remote_post', 'like', 'comment']

    # https://www.django-rest-framework.org/api-guide/relations/#generic-relationships
    def to_representation(self, instance):
        data = super(InboxSerializer, self).to_representation(instance)
        type = ''
        if instance.post:
            type = 'post'
            data = data['post']
        elif instance.follow_request_received:
            type = 'follow'
            data = data['follow_request_received']
        elif instance.remote_post:
            type = 'post'
            data = data['remote_post']
        elif instance.like:
            type = 'like'
            data = data['like']
        elif instance.comment:
            type = 'comment'
            data = data['comment']
        else:
            raise Exception('Unexpected type of inbox item')
        data['type'] = type
        return data

class AddNodeSerializer(serializers.ModelSerializer):
    api_url = serializers.URLField()
    node_name = serializers.CharField()
    team = serializers.ChoiceField(choices=Node.TEAM_CHOICES)
    auth_username = serializers.CharField()
    auth_password = serializers.CharField()
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Author
        fields = ['id', 'api_url', 'password', 'password2', 'auth_username', 'auth_password', 'node_name', 'team']
        read_only_fields = ['id']

    def save(self):
        node_user = Author(
            username=self.validated_data['node_name'], 
            display_name=self.validated_data['node_name'],
            is_remote_user=True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        node_user.set_password(password)
        node = Node(user=node_user, api_url=self.validated_data['api_url'],
                    auth_username=self.validated_data['auth_username'], 
                    auth_password=self.validated_data['auth_password'],
                    team=self.validated_data['team'])
        node_user.save()
        node.save()
        return node_user

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['api_url', 'team', 'auth_username', 'auth_password']

class NodesListSerializer(serializers.ModelSerializer):
    node = NodeSerializer()
    class Meta:
        model = Author
        fields = ['id', 'node', 'password']
