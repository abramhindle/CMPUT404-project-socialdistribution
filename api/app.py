from flask import Flask

app = Flask(__name__)

import api.user.authors


@app.route("/")
def hello_world():
    return {"message": "Hello world"}


if __name__ == '__main__':
    app.run()
