class LocalNodeMiddleware(object):
    """
    Ensures a Node that represents the local server always exists.

    No other suitable hook for code that's run once and can access the server's host name
    was found. A migration was not suitable for the second reason.
    """
    def __init__(self):
        self.local_node_created = False

    def process_request(self, request):
        if not self.local_node_created:
            from dashboard.models import Node
            nodes = Node.objects.filter(local=True)

            host = "http://" + request.get_host()
            if host[-1] != "/":
                host += "/"

            service = host + "service/"

            if len(nodes) == 0:
                node = Node(name="Local", website_url=host, service_url=service, local=True)
                node.save()
            elif len(nodes) == 1:
                node = nodes[0]
                node.host = host
                node.service = service
                node.save()
            else:
                raise RuntimeError("More than one local node found in Nodes table. Please fix before continuing.")

            self.local_node_created = True

        return None
