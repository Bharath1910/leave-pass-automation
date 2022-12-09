from dotenv import  load_dotenv, find_dotenv 
from mfrc522 import SimpleMFRC522
from pymongo import MongoClient
import os, datetime, time
import RPi.GPIO as gpio

# Board setup
gpio.setmode(gpio.BOARD)
gpio.setup(8, gpio.IN)
reader = SimpleMFRC522()

# LED setup
statusLED = 40
approvedLED = 36
rejectedLED = 38

gpio.setup([statusLED, approvedLED, rejectedLED], gpio.OUT)

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

def blink(led):
    gpio.output(led, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(led, gpio.LOW)

gpio.output(statusLED, gpio.HIGH)
print("starting")
while True:
    try:
        try:
            tagID, _ = reader.read()
            data = Fetch(tagID)
        
        except TypeError:
            blink(rejectedLED)
            print("You are not allowed to go!")
        
        else:
            if data.isScanned():
                blink(approvedLED)
                print("Welcome back :)")
                print("You are late: ", data.isLate())
                
            else:
                blink(approvedLED)

                print("updating..")
                data.update()
                print("Happy journey!")
        time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nterminating")
        gpio.output(statusLED, gpio.LOW)
        break

gpio.cleanup()