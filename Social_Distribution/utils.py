import requests
from server.models import Node
from author.serializers import AuthorSerializer
from post.serializers import PostSerializer

def update_authors():
    nodes = Node.objects.all()
    for node in nodes:
        response = requests.get(node.host_url + "authors/", auth=(node.username, node.password))
        try:
            #print("Response")
            #print(response.status_code)
            #print(response.json())
            #print(node.host_url + "authors/")
            authors = response.json()["items"]
            serializer = AuthorSerializer(data=authors, many=True)
            if serializer.is_valid():
                serializer.save()
            #else:
                #print(serializer.error_messages)
        except Exception as e:
            #print("Exception:")
            #print(e)
            continue
    
# pull in remote public posts from other servers
def update_posts(author):
    # /author/{author_id}/posts/
    response = requests.get(author.node.host_url + "author/" + str(author.authorID) + "/posts/", auth=(author.node.username, author.node.password))
    try:
        #print("Response:")
        #print(response.status_code)
        #print(response.text)
        #print(response.json())
        #print(author.node.host_url + "author/" + str(author.authorID) + "/posts/")
        posts = response.json()["items"]
        print(posts)
        serializer = PostSerializer(data=posts, many=True)
        if serializer.is_valid():
            serializer.save()
            print(str(author.authorID))
    except Exception as e:
        pass
        #print("Exception:")
        #print(e)