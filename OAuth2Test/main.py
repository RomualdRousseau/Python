import secrets

from flask import Flask
from oauth import enable_oauth

app = Flask(__name__)
app.secret_key = secrets.token_hex(30)


@app.route('/')
@enable_oauth
def index(userinfo):
    return "Hello " + userinfo["upn"]


if __name__ == '__main__':
    app.run(host="localhost", port=4200)
