import requests
from server.models import Node
from author.serializers import AuthorSerializer

def update_authors():
        nodes = Node.objects.all()
        for node in nodes:
            response = requests.get(node.host_url + "authors/", auth=(node.username, node.password))
            try:
                print("Response")
                print(response.status_code)
                #print(response.json())
                print(node.host_url + "authors/")
                authors = response.json()["items"]
                serializer = AuthorSerializer(data=authors, many=True)
                if serializer.is_valid():
                    serializer.save()
                #else:
                    #print(serializer.error_messages)
            except Exception as e:
                print("Exception:")
                print(e)
                continue