from dotenv import  load_dotenv, find_dotenv # To load environment variables
from pymongo import MongoClient # MongoDB API
import RPi.GPIO as gpio # To access GPIO pins on raspberry pi
import os, datetime 

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

def daysLeft(dateStr):
    curDate = datetime.datetime.now()
    #dateStrObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    leftDays = dateStr - curDate

    return leftDays

def isLate(regNo, collection):
    scn = collection.find_one({"regNo": regNo})
    retrunDate = scn["toDate"]
    curDate = datetime.datetime.now()

    return retrunDate < curDate
    if delDate.days >= 0:
        return False

    elif delDate.days < 0:
        return True



gpio.setup(8, gpio.IN)
print("starting")
while True:
    try:
        if gpio.input(8):
            data = rfidData(2)
            dbData = isScanned(approvedCollection ,data)
            if dbData:
                print(f"Welcome Home {data} \nyou were on leave for: {daysLeft(dbData['lastScanned'])} days\nAre you late?: {isLate(data, approvedCollection)}")
            
            else:
                curTime = datetime.datetime.now()
                updateStr = {
                    "$set": {"lastScanned": curTime}
                }

                approvedCollection.update_one({"regNo": data}, updateStr)
                print("Happy Journey")
        
        else:
            pass
    
    except KeyboardInterrupt:
        print("Terminating!")
        break