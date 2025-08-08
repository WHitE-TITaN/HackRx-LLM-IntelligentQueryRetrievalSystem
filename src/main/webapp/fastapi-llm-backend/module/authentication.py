import os


class Authenticate:
    def __init__(self, uri: str | None = None):
        self.accepted_key = os.getenv("ACCEPTED_KEY")
        self.secondary_key = os.getenv("SECONDARY_KEY")

    def verify_api_key(self, api_key: str) -> bool:
        if api_key == self.accepted_key:
            return True
        if api_key == self.secondary_key:
            return True
        return False


