"""
This is taken from "Simple Usage" page in the docs:
http://sanic-jwt.readthedocs.io/en/latest/pages/simpleusage.html
"""

from sanic import Sanic

from sanic_jwt import exceptions, initialize


class User:
    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


users = [User(1, "user1", "abcxyz"), User(2, "user2", "abcxyz")]

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


app = Sanic()
initialize(
    app,
    authenticate=authenticate,
    cookie_set=True,
    cookie_access_token_name="jwt_access_token",
)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888)
