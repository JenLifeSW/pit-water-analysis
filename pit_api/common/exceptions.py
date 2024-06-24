import json


class BaseException(Exception):
    def __init__(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        super().__init__(message)
        self.message = message


class BadRequest400Exception(BaseException):
    pass


class UnAuthorized401Exception(BaseException):
    pass


class NotFound404Exception(BaseException):
    pass


class Conflict409Exception(BaseException):
    pass
