import os

import pymongo

URI_FORMAT = "mongodb"
HOST = os.environ.get("MONGO_HOST")
USER = os.environ.get("MONGO_USER")
PASS = os.environ.get("MONGO_PASS")

URI = f"{URI_FORMAT}://{USER}:{PASS}@{HOST}"


class MongoConnection:
    def __init__(self):
        self.client = None

    def __del__(self):
        self.close_client()

    def open_client(self):
        if self.client is None:
            self.client = pymongo.MongoClient(URI)

    def close_client(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def get_client(self):
        if self.client is None:
            self.open_client()
        return self.client

mongo_conn = MongoConnection()
