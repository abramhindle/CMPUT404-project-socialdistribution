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
    if author.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
        response = requests.get(author.node.host_url + "author/" + str(author.authorID) + "/posts", auth=(author.node.username, author.node.password))
    else:
        response = requests.get(author.node.host_url + "author/" + str(author.authorID) + "/posts/", auth=(author.node.username, author.node.password))
    try:
        #if str(author.authorID) == "48409866-0811-4ad8-a1d9-29014b4d316d":
        #    print("HERE")
        #print("Response:")
        #print(response.status_code)
        #print(response.text)
        #print(response.json())
        #print(author.node.host_url + "author/" + str(author.authorID) + "/posts/")
        data = response.json()
        if isinstance(data, dict):
            #print("dict")
            posts = data["items"]
        elif isinstance(data, list):
            #print("list")
            posts = data
        #print(posts)
        serializer = PostSerializer(data=posts, many=True)
        if serializer.is_valid():
            serializer.save()
            #print("got: " + str(author.authorID))
        else:
            pass
            #print("did not get: " + str(author.authorID))
            #print(serializer.errors)
    except Exception as e:
        #print("did not get: " + str(author.authorID))
        #print(e)
        pass
        #print("Exception:")
        #print(e)

#def update_followers():
