from .models import Author

import json

def get_author_by_ID(request, id):
	"""
	This function takes a request object and author ID as parameters, it will check if the author is in our database and add the author if it is not.
	"""

	# Decode the request body and load into a json
	body = json.loads(request.body.decode('utf-8'))

	# Check if the foreign ID exists in the database, if not add that Author to our database
	try:
		author = Author.objects.filter(id=id).get()
	except:
		author = Author(
			id = id,
			user = request.user,
			displayName = body["actor"]["displayName"],
			github = body["actor"]["github"],
			host = request.user.host,
			url = body["actor"]["url"]
		)
		author.save()

	return author