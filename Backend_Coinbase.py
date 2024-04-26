from websockets import connect
import asyncio
import sys
import sqlite3
import aiosqlite
import json


conn = sqlite3.connect("./coindata.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS trades")
cursor.execute(""" CREATE TABLE trades(
                        id int PRIMARY KEY,
                        time int,
                        best_bid float,
                        best_ask float)""")

cursor.execute("CREATE INDEX index_time ON trades(time)")

conn.commit()
conn.close()
# Define the URL for Coinbase Pro WebSocket feed
ws_url = "wss://ws-feed.pro.coinbase.com"

# Define the subscription message as a dictionary
subscribe_message = {
    "type": "subscribe",
    "product_ids": ["BTC-USD"],  # Specify the trading pairs you want data for
    "channels": ["ticker"]       # Specify the channel(s) you want data from (e.g. ticker, level2, etc.)
}

# Define an asynchronous function to handle the WebSocket connection
async def coinbase_websocket():
    async with connect(ws_url) as websocket:
        buffer = []
        # Send the subscription message
        await websocket.send(json.dumps(subscribe_message))
        
        print("Subscribed to Coinbase Pro feed")

        # Continuously receive and process messages from the WebSocket connection
        while True:
            # Receive a message from the WebSocket
            message = await websocket.recv()
            data = json.loads(message)
            
            # Handle the received data (e.g. print it)
            print('data :', data)
            #print('data.keys(): ',data.keys())
            #print(data['channels'].keys())
            #print('data[type]: ',data['type'])
            try:
                print('data[best_bid]: ' ,data['best_bid'])
                print('data[best_ask]: ' ,data['best_ask'])
                buffer.append((data['trade_id'],data['time'],data['best_bid'],data['best_ask']))
            except Exception as e:
                print(e)
            
            
            if len(buffer) > 1:

                #print('Writing to DB !!')

                async with aiosqlite.connect("./coindata.db") as db:

                    await db.executemany("""INSERT INTO trades
                                         (id, time, best_bid, best_ask) VALUES (?,?,?,?)""", buffer)
                    await db.commit()
                
                buffer = []

            print(data)

# Run the asynchronous function
asyncio.run(coinbase_websocket())
