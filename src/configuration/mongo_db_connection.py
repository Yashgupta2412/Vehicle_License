import os
import sys
import pymongo
import certifi
from dotenv import load_dotenv
load_dotenv()

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    client=None
    
    def __init__(self,database_name: str=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv("MONGODB_URL")
                if mongo_db_url is None:
                    raise Exception(f"Enviroment variable {MONGODB_URL_KEY} not found.")
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("MongoDB connection is successful.")
        except Exception as e:
            raise MyException(e,sys)
        
       