import os
import sys
from pymongo.mongo_client import MongoClient
from Mainfold.utils.exception import ErrorException
# from ScheduleAI.logger import logging


class MongoDBOp:
    def __init__(self,MONGO_URL,DB_NAME):
        try:
         
         self.Client=MongoClient(MONGO_URL)
         self.database=self.Client[DB_NAME]
         
        except Exception as e:
           raise ErrorException(e,sys)
    
      
    def InsertMany(self,COLLECTION_NAME,Data):
     try:
       
       if isinstance(Data,dict) or isinstance(Data,list):
        inserted_data=self.database[COLLECTION_NAME].insert_many(Data)
        
        return inserted_data
       else:
        
        raise ValueError("data is not in dict format")
       return
     except Exception as e:
        raise ErrorException(e,sys)
    def FetchALL(self,COLLECTION_NAME):
     try:
       
       returned_data=self.database[COLLECTION_NAME].find()
       return returned_data
     except Exception as e:
       raise ErrorException(e,sys)
    def insertOne(self,COLLECTION_NAME,obj):
       try:
         
         collection=self.database[COLLECTION_NAME]
         collection.insert_one(obj)
         
       except Exception as e:
         raise ErrorException(e,sys)
    def findOne(self,COLLECTION_NAME,id):
      try:
       
        collection=self.database[COLLECTION_NAME]
        find_data=collection.find_one(id)
        
        return find_data
        
      except Exception as e:
        raise ErrorException(e,sys)
    

     