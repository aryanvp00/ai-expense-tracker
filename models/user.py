class User:
    # Represents one user
    def __init__(self, username, password_hash, user_id=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def from_mongo(cls, data):
        return cls(
            data["username"],
            data["password_hash"],
            data["_id"]
        )