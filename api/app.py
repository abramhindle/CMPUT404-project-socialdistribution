from flask import Flask

from api.admin import admin_bp
from api.user import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def hello_world():
    return {"message": "Hello world"}


if __name__ == "__main__":
    app.run()
