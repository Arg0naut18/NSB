from motor.motor_asyncio import AsyncIOMotorClient
import os

cluster = AsyncIOMotorClient(os.getenv("MONGO"))

class db:
    database = cluster['NSBUsers']
    economy = database['Users']
    shop_items = database['Shop']
    transactions = database['Transactions']
    notifs = database['Notifications']