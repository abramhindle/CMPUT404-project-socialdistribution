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
def update_posts(author_id):
    nodes = Node.objects.all()
    for node in nodes:
        # /author/{author_id}/posts/
        response = requests.get(node.host_url + "author/" + author_id + "/posts/", auth=(node.username, node.password))
        try:
            print("Response:")
            print(response.status_code)
            print(response.json())
            print(node.host_url + "author/" + author_id + "/posts/")
        except Exception as e:
            print("Exception:")
            print(e)
            continue