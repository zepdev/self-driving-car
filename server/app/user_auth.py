from werkzeug.security import safe_str_cmp

username_table = {}
userid_table = {}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)


class User:
    def __init__(self, id, username, password):
        if username in username_table:
            raise Exception("Username already exists.")

        self.id = id
        if self.id in userid_table:
            raise Exception("ID collision.")

        self.username = username
        self.password = password

        self.__update_tables()

    def __update_tables(self):
        username_table.update({self.username: self})
        userid_table.update({self.id: self})

    def __str__(self):
        return "User(id='%s')" % self.id
