import base64

def generateBasicAuth(username, password):
    credential = str(username) + ":" + str(password)
    credential = credential.encode('utf-8')
    return "Authorization: Basic " + base64.b64encode(credential).decode('utf-8')

if __name__ == "__main__":
    username = input("Please input the username: ")
    password = input("Please input the password: ")
    print(generateBasicAuth(username, password))