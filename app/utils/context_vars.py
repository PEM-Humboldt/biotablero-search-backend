from contextvars import ContextVar

request_id_context = ContextVar("request_id", default=None)
