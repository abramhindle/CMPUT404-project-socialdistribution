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

            service_url = host + "service/"

            if len(nodes) == 0:
                node = Node(name="Local", host=host, service_url=service_url, local=True)
                node.save()
            elif len(nodes) == 1:
                node = nodes[0]
                node.host = host
                node.service_url = service_url
                # TODO: Fix bug that prevents this from actually saving
                node.save()
            else:
                raise RuntimeError("More than one local node found in Nodes table. Please fix before continuing.")

            self.local_node_created = True

        return None
