from dotenv import  load_dotenv, find_dotenv # To load environment variables
from RPi.GPIO import GPIO as gpio # To access GPIO pins on raspberry pi
from pymongo import MongoClient # MongoDB API
import os # To access environment variables

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

def isScanned(collection, regNo):
    scn = collection.find_one({"regNo": f"{regNo}","lastScanned": {"$exists": True}})
    
    if scn == None:
        return False
    
    return True

def rfidData(temp):
    if temp == 1:
        return "22BEC7194"
    
    elif temp == 2:
        return "21BCE7194"
    
    else:
        return "19BCE1234"

