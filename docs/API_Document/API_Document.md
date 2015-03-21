<b>API DOCUMENTATION</b>
<br/>
The SocialDistribution API allows for developers looking to get access to posts, make friend requests, and check statuses of friendships from the SocialDistribution network.
<br/><p>
If you wish to use this API, please email nbui@ualberta.ca(or any of the other group members) for the http authentication password. 
<br/><br/>
The following are URIs that can be used:<br/>
<i>Note: Not officially deployed yet. Hence, “Service” will be modified later</i>
<br/>
1 http://service/api/posts<br/>
2 http://service/api/posts/{POST_ID}<br/>
3 http://service/api/author/posts<br/>
4 http://service/api/author/{AUTHOR_ID}/posts<br/>
5 http://service/api/friendrequest<br/>
6 http://service/api/friends/{AUTHOR_ID}<br/>
7 http://service/api/friends/{FRIEND_ID}/{FRIEND_ID}<br/>
<br/></p><p>
##1.http://service/api/posts<br/>
Method: Get all posts marked as public on the server<br/>
Example:<br/>
Request:<br/>
<br/>

    GET /api/posts HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

<br/>
Output: [list of results]<br/>
Response:<br/>

    {
    "post": [
    {
        "origin": "http://whereitcamefrom.com/post/zzzzz",
        "description": "description here",
        "pubDate": "2015-03-11 04:08:54.183383",
        "title": "titlehere",
        "author": {
            "url": "localhost:8000/author/1",
            "host": "localhost:8000",
            "displayname": "n",
            "id": "1"
        },
      	        "comments":[
                    {
                    	 "author":{
                       		 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                        	 "host":"http://127.0.0.1:5454/",
                        	"displayname":"Greg"
                   	 },
                   	"comment":"Sick Olde English"
                    	"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    	"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
                }]
        "content": "status updated",
        "source": "http://lastplaceigotthisfrom.com/post/yyyyy",
        "visibility": "public",
        "content_type": "text/plain",
        "guid": "54f446b4-c7a4-11e4-b490-080027dc431b",
        "categories": []
        }, 
       {
       	 "origin": "http://whereitcamefrom.com/post/zzzzz",
       	 "description": "description2",
       	 "pubDate": "2015-03-11 04:45:55.432936",
       	 "title": "title2",
       	 "author": {
            	"url": "localhost:8000/author/1",
           	 	"host": "localhost:8000",
           	 	"displayname": "n",
            	"id": "1"},
       	 },
      	 "comments":[{
                    	 "author":{
                       		 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                        	 "host":"http://127.0.0.1:5454/",
                        	"displayname":"Greg"
                   	 },
                   	"comment":"Sick Olde English"
                    	"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    	"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
              }]
       	 "content": "status2",
       	 "source": "http://lastplaceigotthisfrom.com/post/yyyyy",
       	 "visibility": "public",
       	 "content_type": "text/plain",
      	  "guid": "80ec14ae-c7a9-11e4-a504-080027dc431b",
       	 "categories": []
       }]
    }


</p><p>
   
##2.http://service/api/posts/{POST_ID}<br/>
Method: Get a single post with id = {POST_ID}<br/>
Example:<br/>
Request:

    GET /api/posts/108ded43-8520-4035-a262-547454d32022 HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

<br/>
Output: a single post<br/>
Response:<br/>

    {
        "posts":[
        {
            "title":"A post title about a post about web dev",
            "source":"http://lastplaceigotthisfrom.com/post/yyyyy",
            "origin":"http://whereitcamefrom.com/post/zzzzz",
            "description":"This post discusses stuff -- brief",
            "content-type":"text/html",
            "content":"hello this is a message",
            "author":{
                "id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayname":"Lara",
                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
            },
            "categories":["web","tutorial"],
            "comments":[{
                   		 "author":{
                       			 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                      			  "host":"http://127.0.0.1:5454/",
                       			 "displayname":"Greg"
                  		},
                    		"comment":"Sick Olde English"
                   		"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    		"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
           }]
           "pubDate":"Fri Jan  1 12:12:12 MST 2014",
            "guid":"108ded43-8520-4035-a262-547454d32022"
            "visibility":"PUBLIC"                                           
        }]
    }

</p><p>
##3.http://service/api/author/posts<br/>
Method: Get all posts that are visible to the currently authenticated user<br/>
Example:<br/>
Request:

    GET /api/author/posts/ HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

<br/>
Output: [list of results]<br/>
Response:<br/>

    {
        "post": [
           {
             "origin": "http://whereitcamefrom.com/post/zzzzz",
             "description": "description here",
             "pubDate": "2015-03-11 04:08:54.183383",
             "title": "titlehere",
             "author": {
                          "url": "localhost:8000/author/1",
                          "host": "localhost:8000",
                          "displayname": "n",
                          "id": "1"
             },
             "comments":[
                        {
                          "author":{
                       		 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                        	 "host":"http://127.0.0.1:5454/",
                        	 "displayname":"Greg"
                   	   },
                   	"comment":"Sick Olde English"
                    	"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    	"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
             }]
             "content": "status updated",
             "source": "http://lastplaceigotthisfrom.com/post/yyyyy",
             "visibility": "public",
             "content_type": "text/plain",
             "guid": "54f446b4-c7a4-11e4-b490-080027dc431b",
             "categories": []
             }, 
        ]
    }

</p><p>
##4. http://service/api/author/{AUTHOR_ID}/posts<br/>
Method: Get all posts made by {AUTHOR_ID} visible to the currently authenticated user<br/>
Example:<br/>
Request:

    GET /api/author/posts/8d919f29c12e8f97bcbbd34cc908f19ab9496989 HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

<br/>
Output: [list of results]<br/>
Response:<br/>

    {
      “post": [
        {
        "origin": "http://whereitcamefrom.com/post/zzzzz",
        "description": "description here",
        "pubDate": "2015-03-11 04:08:54.183383",
        "title": "titlehere",
        "author": {
            "url": "localhost:8000/author/1",
            "host": "localhost:8000",
            "displayname": "n",
            "id": "1"
        },
      	        "comments":[
                    {
                    	 "author":{
                       		 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                        	 "host":"http://127.0.0.1:5454/",
                        	"displayname":"Greg"
                   	 },
                   	"comment":"Sick Olde English"
                    	"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    	"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
                }]
        "content": "status updated",
        "source": "http://lastplaceigotthisfrom.com/post/yyyyy",
        "visibility": "public",
        "content_type": "text/plain",
        "guid": "54f446b4-c7a4-11e4-b490-080027dc431b",
        "categories": []
        }, 
       {
       	 "origin": "http://whereitcamefrom.com/post/zzzzz",
       	 "description": "description2",
       	 "pubDate": "2015-03-11 04:45:55.432936",
       	 "title": "title2",
       	 "author": {
            	"url": "localhost:8000/author/1",
           	 	"host": "localhost:8000",
           	 	"displayname": "n",
            	"id": "1"},
       	 },
      	 "comments":[{
                    	 "author":{
                       		 "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                        	 "host":"http://127.0.0.1:5454/",
                        	"displayname":"Greg"
                   	 },
                   	"comment":"Sick Olde English"
                    	"pubDate":"Fri Jan  3 15:50:40 MST 2014",
                    	"guid":"5471fe89-7697-4625-a06e-b3ad18577b72"
              }]
       	 "content": "status2",
       	 "source": "http://lastplaceigotthisfrom.com/post/yyyyy",
       	 "visibility": "public",
       	 "content_type": "text/plain",
      	  "guid": "80ec14ae-c7a9-11e4-a504-080027dc431b",
       	 "categories": []
        }]
    }



   
</p><p>
##5. http://service/api/friendrequest<br/>
Method: makes a friend request post<br/>
Example:<br/>
Request:

    POST /api/friendrequest HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

    {
        "query": "friendrequest",
	"author":{
		"id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
		"host":"http://127.0.0.1:5454/",
		"displayname":"Greg"
	},
	"friend": {
		"id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
		"host":"http://127.0.0.1:5454/",
		"displayname":"Lara",
		"url":"http://127.0.0.1:5454/author/
          9de17f29c12e8f97bcbbd34cc908f1baba40658e"
	}
    }

<br/>
Output: none<br/>
Response:

    HTTP/1.1 200 OK


</p><p>
##6. http://service/api/friends/{AUTHOR_ID}<br/>
Method: Posts all the authors in the list who are friends with the author<br/>
Endpoint: api/author/friends/{AUTHOR_ID}<br/>
Example:<br/>
Request:

    POST /api/author/friends/9de17f29c128f97bcbbd34cc908f1baba40658e HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

    {
      "query":"friends",
      "author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
      "authors":
      [
	"7deee0684811f22b384ccb5991b2ca7e78abacde",
	"31cc28a8fbc05787d0470cdbd62ea0474764b0ae",
	"1af17e947f387a2d8c09a807271bd094e8eff077",
	"77cb4f546b280ea905a6fdd99977cd090613994a",
	"11c3783f15f7ade03430303573098f0d4d20797b",
	"bd9ef9619c7241112d2a2b79505f736fc8d7f43e",
	"0169a8ebf3cb3bd7f092603564873e12cce9d4c5",
	"2130905fd0de94c3379e04839cd9f6889ba2b52c",
	"b32c9e0b5fcf85f46b9ce2ba89b2068b57d4641b",
	"fe45075b93d06c833bb25d5a6dfe669cfde3f99d",
	"e28e59a9612c369717f66f53f3e014b341857601",
	"b36e52d6aaee9285220f94fc321407a44e4dc622",
	"584a9739ea459ce4aae5a88827d970196fb27769",
	"96b3b5a70cd9591c73760bd8669aa5bd7cc689c5",
	"6465678d0a409b96829fd64d0894132966e97eee",
	"695c780ea2815bc94c54782f5046dfa4e325f875",
	"8743f7511a1a569e4e9dacbb25e27395629ba5c0",
	"539b65f2d76d0327dc45bf6354cda535d6f8ed02",
	"c55670261253c5ce25e22b47a34629dd15e819d4"
      ]
    }
<br/>
Output: [list of results]<br/>
Response:

    {
        "query":"friends",
	"author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
	"friends":[
		"7deee0684811f22b384ccb5991b2ca7e78abacde",
		"11c3783f15f7ade03430303573098f0d4d20797b",
	]
    }

</p><p>
##7. http://service/api/friends/{AUTHOR_ID}/{Author_ID}<br/>
Method: Responds if the authors are friends or not<br/>
Example:<br/>
Request:

    GET /api/author/friends/9de17f29c12e8f97bcbbd34cc908f1baba40658e/8d919f29c12e8f97bcbbd34cc908f19ab9496989 HTTP/1.1
    HOST: service
    Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    Content-Type: application/json

<br/>
Response:

     {
        "query":"friends",
	"authors":[
                 "9de17f29c12e8f97bcbbd34cc908f1baba40658e",
	         "8d919f29c12e8f97bcbbd34cc908f19ab9496989"
        ],
        "friends":"YES" # or “NO”
    }



</p>
