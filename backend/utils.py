from manager.settings import HOSTNAME
from .models import Author, Node

import json

def get_author_by_ID(request, id, label):
	"""
	This function takes a request object and author ID as parameters, it will check if the author is in our database and add the author if it is not. Returns the author object and a boolean representing if it is local or remote.
	"""

	# Decode the request body and load into a json
	body = json.loads(request.body.decode('utf-8'))

	# Check if the foreign ID exists in the database, if not add that Author to our database
	try:
		author = Author.objects.filter(id=id).get()

		if author.host == HOSTNAME:
			return author, True
		else:
			return author, False
	except:

		node = Node.objects.filter(host=body[label]["host"]).get()

		print(body[label]["displayName"])

		author = Author(
			id = id,
			user = node.user,
			displayName = body[label]["displayName"],
			github = body[label]["github"],
			host = body[label]["host"],
			url = body[label]["url"]
		)
		author.save()
		return author, False
