from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()


def connect_mongo():
    connect(
        db=os.getenv("MONGO_DB"),
        host=f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.xik54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        ssl=True,
    )
