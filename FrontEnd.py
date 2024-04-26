from dash import html, dcc, Output, Input, Dash, State
import dash_bootstrap_components as dbc
import sqlite3
import time
import math


app = Dash(external_stylesheets=[dbc.themes.MINTY])


app.layout = html.Div([
   
    html.Div([
       
        html.H1("Streaming Cross Exchange Arbitrage",style={'margin-left': '70px'}),
        
       
    ], style={'display': 'flex', 'align-items': 'center',"padding-top":"120px"}),

    html.Div([
      
        html.Hr(style={'borderWidth': "2vh", "width": "100%", "borderColor": "#3C7637","opacity": "unset"}),
        
       
    ], style={'display': 'flex', 'align-items': 'center',"padding-top":"10px"}),

    html.Div([
       
        html.Label("Timestamp:",style={'margin-left': '70px'}),
        
        # Output component
        html.Plaintext(id='timestamp', style={'margin-left': '35px'})  
    ], style={'display': 'flex', 'align-items': 'center',"padding-top":"40px"}),

    html.Div([
      
        html.Label("Bitcoin BTC/USDT BID Price:",style={'margin-left': '70px'}),
        
        # Output component
        html.Plaintext(id='bitcoin_bid', style={'margin-left': '35px'})  
    ], style={'display': 'flex', 'align-items': 'center',"padding-top":"40px"}),

    html.Div([
      
        html.Label("Bitcoin BTC/USDT ASK Price:",style={'margin-left': '70px'}),
        
        # Output component
        html.Plaintext(id='bitcoin_ask', style={'margin-left': '35px'}) 
    ], style={'display': 'flex', 'align-items': 'center'}),

    html.Div([
       
        html.Label("CoinBase BTC/USDT BID Price:",style={'margin-left': '70px'}),
        
        # Output component
        html.Plaintext(id='coinbase_bid', style={'margin-left': '20px'})  
    ], style={'display': 'flex', 'align-items': 'center'}),

    html.Div([
     
        html.Label("CoinBase BTC/USDT ASK Price:",style={'margin-left': '70px'}),
        
        # Output component
        html.Plaintext(id='coinbase_ask', style={'margin-left': '20px'})  
    ], style={'display': 'flex', 'align-items': 'center'}),


    html.Div([
        
        html.Label("Go Long on CoinBase and Short on Binance: ",style={'margin-left': '70px'}),
        
        # Output component 
        html.Plaintext(id='Coin_Ask_Bit_Bid', style={'margin-left': '20px'})  
    ], style={'display': 'flex', 'align-items': 'center'}),


    html.Div([
       
        html.Label("Go Long on Binance and Short on CoinBase: ",style={'margin-left': '70px'}),
        
        # Output component 
        html.Plaintext(id='Bit_Ask_Coin_Bid', style={'margin-left': '20px'})  
    ], style={'display': 'flex', 'align-items': 'center'}),

        # Regreah Rate = 100ms
        dcc.Interval(id="update", interval = 100),

                      ])



@app.callback(  
    Output("timestamp","children"),
    Output("bitcoin_bid", "children"),
    Output("bitcoin_ask", "children"),
    Output("coinbase_bid", "children"),
    Output("coinbase_ask", "children"),
    Output("Coin_Ask_Bit_Bid","children"),
    Output("Bit_Ask_Coin_Bid","children"),

    Input("update", "n_intervals"),
)
def update_data(intervals):


    conn = sqlite3.connect("./data.db")
    cursor = conn.cursor()

    data = cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 1").fetchall()

    binance_best_bid = data[0][1]
    binance_best_ask = data[0][2]

    conn2 = sqlite3.connect("./coindata.db")
    cursor2 = conn2.cursor()

    data2 = cursor2.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 1").fetchall()

    coin_best_bid = data2[0][2]
    coin_best_ask = data2[0][3]

    Coin_Ask_Bit_Bid = data2[0][3] - data[0][1]
    Bit_Ask_Coin_Bid = data[0][2] - data2[0][2]

    timestamp = data2[0][1]   
    

    # (new data, trace to add data to, number of elements to keep)
    return timestamp, binance_best_bid,binance_best_ask,coin_best_bid,coin_best_ask, Coin_Ask_Bit_Bid,Bit_Ask_Coin_Bid

if __name__ == "__main__":
    app.run_server(debug=True)