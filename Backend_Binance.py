from websockets import connect
import asyncio
import sys
import sqlite3
import aiosqlite
import json


conn = sqlite3.connect("./data.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS trades")
cursor.execute(""" CREATE TABLE trades(
                        id int PRIMARY KEY,
                        best_bid float,
                        best_ask float)""")



conn.commit()
conn.close()

url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"

async def save_data(url):

    async with connect(url) as websocket:
        
        buffer = []
        
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            buffer.append((data['u'],data['b'],data['a']))

            #print(data)

            if len(buffer) > 1:

                #print('Writing to DB !!')

                async with aiosqlite.connect("./data.db") as db:

                    await db.executemany("""INSERT INTO trades
                                         (id, best_bid,best_ask) VALUES (?,?,?)""", buffer)
                    await db.commit()
                
                buffer = []

            print(data)


asyncio.run(save_data(url))