from typing import Tuple


class Response:
    def __init__(self, code: int, status: str, message: str | None = None, payload: dict | None = None):
        self.code = code
        self.status = status
        self.payload = payload
        self.message = message

    def to_response(self) -> Tuple[dict, int]:
        return {
            "payload": self.payload,
            "status": self.status,
            "message": self.message
        }, self.code