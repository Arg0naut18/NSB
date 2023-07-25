from motor.motor_asyncio import AsyncIOMotorClient
import json

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
srv = vari["mongo"]

cluster = AsyncIOMotorClient([srv])

class db:
    db = cluster['NSBUsers']
    economy = db['Users']
    shopItems = db['Shop']