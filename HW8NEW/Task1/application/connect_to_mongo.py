from mongoengine import connect


def connect_mongo():
    connect(
        db="mydb",
        host="mongodb+srv://barabaca:280992@cluster0.xik54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        ssl=True,

    )
