from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *

import json
# check create author + get author(s)
class TestAuthor(APITestCase):
    # tests the get and multi-get function of the author view
    def test_get_author(self):
        # create the author first so we can have the ID
        create_author = Author.objects.create(displayName='sugon')
        Author.objects.create(displayName='sawcon')
        test_id = str(create_author).split('(')
        
        test_id = test_id[-1].strip(')')
        user_url = reverse('authors:get_authors') + test_id + '/'
        
        # the single get for sugon
        response = self.client.get(user_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon")
        # check if the multi-get contains sawcon and sugon
        response = self.client.get(reverse('authors:get_authors'))
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon")
        self.assertContains(response,"sawcon")

    def test_individualauthorget(self):
        '''Testing the GET request for an individual author'''
        create_author = Author.objects.create(displayName='sugon')
        test_id = str(create_author).split('(')
        test_id = test_id[-1].strip(')')
        user_url = reverse('authors:detail',kwargs={'pk_a':test_id})
        
        response = self.client.get(user_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon")

        #authordoesnotexist
        user_url += "4"
        response = self.client.get(user_url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        

        

    # tests the put function of the author view
    def test_put_update_author(self):
        # create the author first so we can have the ID
        create_author = Author.objects.create(displayName='sugon')
        test_id = str(create_author).split('(')
        test_id = test_id[-1].strip(')')
        user_url = reverse('authors:get_authors') + test_id + '/'
        # test the put
        response = self.client.put(user_url,{'displayName':'sawcon'})
        
        
        # returns the 200?
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # is named sawcon instead of sugon?
        self.assertNotContains(response,"sugon")
        self.assertContains(response,"sawcon")




    #tests following and checking inbox after the author you followed made a post
    '''def test_follow_and_inbox(self):
        create_author = Author.objects.create(displayName='sugon')
        test_name= str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        #user_url = reverse('authors:get_authors') + test_id + '/'
        create_author2 = Author.objects.create(displayName='sawcon')
        test_id2 = str(create_author2).split('(')
        test_id2 = test_id2[-1].strip(')')

        url = reverse('authors:follow',kwargs={'pk_a':test_id,'pk':test_id2})
        response = self.client.put(url,{'displayName':'sawcon'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # set up the json object with that data
        author_data = {
            'id':test_id,
            'displayName':test_name[0].strip(),
        }
        post_data = {
            'author':author_data,
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        
        # test the post
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        url = reverse('authors:inbox',kwargs={'pk_a':test_id2})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)'''



    

    #tests following and checking inbox after the author you followed made a post
    def test_follow_and_inbox(self):
        '''This function tests for the following
            1) Seeing all the followers of an author
            2) Seeing an individual follower of an author
            3) Checking inbox of the follower after the followed makes a post
            4) Deleting the followers and then checking if the follower list is empty'''
        create_author = Author.objects.create(displayName='sugon')
        test_name= str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        #user_url = reverse('authors:get_authors') + test_id + '/'
        create_author2 = Author.objects.create(displayName='sawcon')
        test_id2 = str(create_author2).split('(')
        test_id2 = test_id2[-1].strip(')')

        url = reverse('authors:follow',kwargs={'pk_a':test_id,'pk':test_id2})
        response = self.client.put(url,{'displayName':'sawcon'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #Testing for 2
        response = self.client.get(url)
    
        #Testing for 1
        url = reverse('authors:get_followers',kwargs = {'pk_a': test_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sawcon")

        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # set up the json object with that data
        author_data = {
            'id':test_id,
            'displayName':test_name[0].strip(),
        }
        post_data = {
            
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        
        # testing for 3
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        url = reverse('authors:inbox',kwargs={'pk_a':test_id2})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #Testing for 4
        url = reverse('authors:follow',kwargs={'pk_a':test_id,'pk':test_id2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotContains(response,"sawcon")

    
    def test_follow_req(self):
        '''tests if a follow request is successfully sent and accessible through GET'''
        create_author = Author.objects.create(displayName='sugon')
        test_name= str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        #user_url = reverse('authors:get_authors') + test_id + '/'
        create_author2 = Author.objects.create(displayName='sawcon')
        test_id2 = str(create_author2).split('(')
        test_id2 = test_id2[-1].strip(')')

        post_data =  {
        "type": "Follow",
        "actor":{"id":test_id},
        "object":{"id":test_id2}
        }
        url = reverse('authors:inbox',kwargs={'pk_a':test_id})
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")


        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #Check for sending a request thats already sent
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertContains(response,"You've already sent a request to this user!")

        #Following yourself test
        post_data =  {
        "type": "Follow",
        "actor":{"id":test_id},
        "object":{"id":test_id}
        }
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertContains(response,"You cannot send a follow request to yourself!")



        #viewing the sent req
        url = reverse('authors:inbox',kwargs={'pk_a':test_id2})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon wants to follow sawcon")
        