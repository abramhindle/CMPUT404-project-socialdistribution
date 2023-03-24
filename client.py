import requests
import base64

def getNodeAuthors_social_distro():

    #https://social-distro.herokuapp.com/api/authors/15/
    url = 'https://social-distro.herokuapp.com/api/authors/'

    username = 'remote1'
    password = 'r3mot31'
    #remote1:r3mot31
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}

    response = requests.get(url, headers=headers)
   
    status_code = response.status_code
    json_response = response.json()
    authors = json_response['results']
    return authors



def getNodeAuthors_Yoshi():


    url = 'https://yoshi-connect.herokuapp.com/authors'

    #base64encoded username: minion and password: minion
    # authorization = 'minion:minion'
    # encoded_authorization = base64.b64encode(authorization.encode("utf-8"))
    # authroization_header = 'Basic ' + encoded_authorization
    # headers = {'Authorization': authroization_header}
    
    response = requests.get(url)
    status_code = response.status_code
    # response = requests.get(url, headers=headers)
    json_response = response.json()
    authors = json_response['items']

    return authors






def getNodeAuthor_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id

    response = requests.get(url)
    status_code = response.status_code
    
    if status_code == 200:
        json_response = response.json()
       
        return(json_response, status_code)
    else: return (None, status_code)



#29c546d45f564a27871838825e3dbecb
# getNodeAuthor_Yoshi('asgasdfgdsfgd')
# getNodeAuthor_Yoshi('29c546d45f564a27871838825e3dbecb')

def getNodeAuthor_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/https://social-distro.herokuapp.com/authors/'

    url = url + author_id

    response = requests.get(url)
    status_code = response.status_code
   
    if status_code == 200:
        json_response = response.json()

        return(json_response, status_code)
    else: return (None, status_code)


####### GET POSTS

def getNodePost_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id + '/posts/'
    
    response = requests.get(url)
    status_code = response.status_code
   
    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)

#29c546d45f564a27871838825e3dbecb
# getNodeAuthor_Yoshi('asgasdfgdsfgd')
# getNodeAuthor_Yoshi('29c546d45f564a27871838825e3dbecb')

def getNodePost_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/'

    url = url + author_id + '/posts/'
    username = 'remote1'
    password = 'r3mot31'
    #remote1:r3mot31
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}

    response = requests.get(url, headers=headers)
    #response = requests.get(url)
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        return(json_response)

# import socket

# bytes_to_read = 4096
# HOST = 'yoshi-connect.herokuapp.com'

# def get(port):

#     request = b"GET /authors HTTP/1.1\nHost:" + HOST.encode("utf-8") + b"\n\n"

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, port))
#     s.send(request)

#     s.shutdown(socket.SHUT_WR)

#     result = s.recv(bytes_to_read)
#     print(result.decode())
#     # while(len(result) > 0):

#     #         print(result)
#     #         result = s.recv(bytes_to_read)
#     s.close()


    
# get(80)