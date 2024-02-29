import time


class User:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
        self.is_muted: bool = False
        self.is_trusted: bool = False
        self.unmute_time: float = 0

    def is_time_to_umnute(self) -> bool:
        return time.time() > self.unmute_time


class UserStorage:
    users: dict[int, User] = {}

    def __init__(self) -> None:
        pass

    @classmethod
    def get_user(cls, user_id: int) -> User:
        if user_id in cls.users:
            user = cls.users[user_id]
        else:
            user = User(user_id)
            cls.users.update({user_id: user})
        return user


def trust(user: User) -> None:
    user.is_trusted = True


def mute(user: User) -> None:
    user.is_muted = True
    user.unmute_time = time.time() + 60


def unmute(user: User) -> None:
    user.is_muted = False
