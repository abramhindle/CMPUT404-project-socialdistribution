import base64
a = input("Please input your username:")
b = input("Please input your password:")
c = str(a) + ":" + str(b)
c = c.encode('utf-8')
print("Authorization: Basic", base64.b64encode(c).decode('utf-8'))
