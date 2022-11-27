from dotenv import  load_dotenv, find_dotenv # To load environment variables
from pymongo import MongoClient # MongoDB API
import os, datetime 

# Loading the environment variables
load_dotenv(find_dotenv())

dbUsr = os.environ.get("MONGODB_USR")
dbPwd = os.environ.get("MONGODB_PWD")

# Getting the database
# db = client.leavePass
# approvedCollection = db.approved

class Fetch:
    def __init__(self, regNo):
        client = MongoClient(f"mongodb+srv://{dbUsr}:{dbPwd}@cluster0.w25vf.mongodb.net/?retryWrites=true&w=majority").leavePass.approved
        self.data = client.find_one({"regNo": regNo})
    
    def out(self):
        return self.data
    
    def isScanned(self):
        try:
            self.data["lastScanned"]
            return True
        
        except KeyError:
            return False


approvedDB = Fetch("22BEC7194")

print(approvedDB.isScanned())





def isScanned(collection, regNo):
    scn = collection.find_one({"regNo": f"{regNo}","lastScanned": {"$exists": True}})
    
    if scn == None:
        return False
    
    return scn

def rfidData(temp):
    if temp == 1:
        return "22BEC7193"
    
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

# data = rfidData(2)
# document = approvedCollection.find_one({"regNo": data})

# dbData = isScanned(approvedCollection ,data)
# if dbData:
#     print(f"Welcome Home {data} \nyou were on leave for: {daysLeft(dbData['lastScanned'])} days\nAre you late?: {isLate(data, approvedCollection)}")

# else:
#     curTime = datetime.datetime.now()
#     updateStr = {
#         "$set": {"lastScanned": curTime}
#     }
#     approvedCollection.update_one({"regNo": data}, updateStr)
#     print("Happy Journey")