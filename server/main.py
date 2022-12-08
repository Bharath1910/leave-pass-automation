from dotenv import  load_dotenv, find_dotenv 
from mfrc522 import SimpleMFRC522
from pymongo import MongoClient
import RPi.GPIO as gpio
import os, datetime

gpio.setmode(gpio.BOARD)
gpio.setup(8, gpio.IN)
reader = SimpleMFRC522()

# Loading the environment variables
load_dotenv(find_dotenv())
dbUsr = os.environ.get("MONGODB_USR")
dbPwd = os.environ.get("MONGODB_PWD")

client = MongoClient(f"mongodb+srv://{dbUsr}:{dbPwd}@cluster0.w25vf.mongodb.net/?retryWrites=true&w=majority").leavePass.approved

class Fetch:
    def __init__(self, tagID):
        """
        The Fetch class is used to get details about the students
        which will be useful for confirming their leave just by 
        inputting their registration number.
        """

        self.tagID = tagID
        self.curTime = datetime.datetime.now()
        self.data = client.find_one({"tagID": self.tagID})
        self.regNo = self.data["regNo"]

    def isScanned(self):
        """
        The isScanned method outputs a boolen, it will return
        True if the student already scanned the RFID reader and 
        now he/she is scanning again to confirm that they 
        returned, and it will return False if the student
        didn't left the campus yet.
        """

        try:
            self.data["lastScanned"]
            return True
        
        except KeyError:
            return False

    def update(self):
        """
        The update method is used to update the current
        time when the student first scans the RFID reader.
        """

        updateString = {
            "$set": {
                "lastScanned": self.curTime
            }
        }

        client.update_one({"regNo": self.regNo}, updateString)
    
    def isLate(self):
        """
        The isLate method returns a boolean, it will 
        return True if the student reported to the 
        university late, and it will return False
        if the student reported to the university 
        on time.
        """
        
        returnDate = self.data["toDate"]
        curDate = self.curTime

        return returnDate < curDate

print("starting")
while True:
    try:
        try:
            tagID, _ = reader.read()
            data = Fetch(tagID)
        
        except TypeError:
            print("You are not allowed to go!")
        
        else:
            if data.isScanned():
                print("Welcome back :)")
                print("You are late: ", data.isLate())
                
            else:
                print("updating..")
                data.update()
                print("Happy journey!")
    
    except KeyboardInterrupt:
        print("terminating")
        break