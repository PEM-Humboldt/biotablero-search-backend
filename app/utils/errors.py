class ServerError(Exception):
    def __init__(self, code: int, usr_msg: str, e: Exception):
        self.code = code
        self.usr_msg = usr_msg
        super().__init__(e)


class NotFoundError(Exception):
    def __init__(self, log_msg, usr_msg: str, e: Exception | None = None):
        self.log_msg = log_msg
        self.usr_msg = usr_msg
        super().__init__(e)
