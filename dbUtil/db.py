from motor.motor_asyncio import AsyncIOMotorClient
import json

j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
srv = vari["mongo"]

cluster = AsyncIOMotorClient([srv])

class db:
    db = cluster['NSBUsers']
    economy = db['Users']
    shopItems = db['Shop']
    transactions = db['Transactions']
    notifs = db['Notifications']