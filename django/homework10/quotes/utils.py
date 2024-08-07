from pymongo import MongoClient


def get_database():
    client = MongoClient(
        "mongodb+srv://user01:26100510@cluster0.yzrztho.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client.home_work10
    return db
