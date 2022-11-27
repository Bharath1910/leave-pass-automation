from dotenv import  load_dotenv, find_dotenv # To load environment variables
from pymongo import MongoClient # MongoDB API
import RPi.GPIO as gpio # To access GPIO pins on raspberry pi
import os # To access environment variables

# Setting up GPIO in raspberry pi
gpio.setmode(gpio.BOARD)

# Loading the environment variables
load_dotenv(find_dotenv())

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
    
    return scn

def rfidData(temp):
    if temp == 1:
        return "22BEC7194"
    
    elif temp == 2:
        return "21BCE7194"
    
    else:
        return "19BCE1234"

gpio.setup(8, gpio.IN)
print("starting")
while True:
    try:
        if gpio.input(8):
            data = rfidData(1)
            dbData = isScanned(approvedCollection ,data)
            if dbData:
                print(f"Welcome Home {data} \nyou left the campus on: {dbData['lastScanned']}")
            
            else:
                print("Happy Journey")
        
        else:
            pass
    
    except KeyboardInterrupt:
        print("Terminating!")
        break