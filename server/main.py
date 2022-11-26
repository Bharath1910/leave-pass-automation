from dotenv import  load_dotenv, find_dotenv
from pymongo import MongoClient
import os, pprint

load_dotenv(find_dotenv())

# Loading the environment variables
dbUsr = os.environ.get("MONGODB_USR")
dbPwd = os.environ.get("MONGODB_PWD")

# Connecting to the database
connectionString = f"mongodb+srv://{dbUsr}:{dbPwd}@cluster0.w25vf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connectionString)

# Getting the database
db = client.leavePass
approvedCollection = db.approved