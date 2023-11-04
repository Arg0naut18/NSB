from motor.motor_asyncio import AsyncIOMotorClient
import json
from configs import MONGO

cluster = AsyncIOMotorClient([MONGO])

class db:
    database = cluster['NSBUsers']
    economy = database['Users']
    shop_items = database['Shop']
    transactions = database['Transactions']
    notifs = database['Notifications']