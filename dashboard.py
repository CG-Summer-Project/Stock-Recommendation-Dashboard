import dash
import dash_core_components as dcc   
import dash_html_components as html 
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import pandas as pd
from dash.exceptions import PreventUpdate

## Functions for calculating SMA, EMA, MACD, RSI
def SMA(data, period = 100, column = 'Close'):
        return data[column].rolling(window=period).mean()

def EMA(data, period = 20, column = 'Close'):
        return data[column].ewm(span=period, adjust = False).mean()

def MACD(data, period_long = 26, period_short = 12, period_signal = 9, column = 'Close'):
        shortEMA = EMA(data, period_short, column=column)
        longEMA = EMA(data, period_long, column=column)
        data['MACD'] = shortEMA - longEMA
        data['Signal_Line'] = EMA(data, period_signal, column = 'MACD')
        return data

def RSI(data, period = 14, column = 'Close'):
        delta = data[column].diff(1)
        delta = delta[1:]
        up = delta.copy()
        down = delta.copy()
        up[up<0] = 0
        down[down>0] = 0
        data['up'] = up
        data['down'] = down
        avg_gain = SMA(data, period, column = 'up')
        avg_loss = abs(SMA(data, period, column = 'down'))
        RS = avg_gain/avg_loss
        RSI = 100.0 - (100.0/(1.0+RS))
        data['RSI'] = RSI
        return data


def get_stock_price_fig(df,v2,v3):

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.035,
    row_width=[0.1, 0.1,0.1, 0.3],subplot_titles=("", "", "", ""))

    fig.add_trace(go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],showlegend = False, name = 'Price'),row=1,col=1)

    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'],opacity=0.5,showlegend = False, name = 'Volume'),
    row = 2, col= 1)

    # Indicators
    if v2=='RSI':
        fig.add_trace(go.Scatter(x = df['Date'], y=df['RSI'], mode="lines", name = 'RSI'),
        row = 3, col= 1)
        fig.layout.xaxis.showgrid=False
    elif v2=='SMA':
        fig.add_trace(go.Scatter(x = df['Date'], y=df['SMA'], mode="lines", name = 'SMA'),
        row = 3, col= 1)
        fig.layout.xaxis.showgrid=False
    elif v2=='EMA':
        fig.add_trace(go.Scatter(x = df['Date'], y=df['EMA'], mode="lines", name = 'EMA'),
        row = 3, col= 1)
        fig.layout.xaxis.showgrid=False
    elif v2=='MACD':
        fig.add_trace(go.Scatter(x = df['Date'], y=df['MACD'], mode="lines",name = 'MACD'),
        row = 3, col= 1)
        fig.add_trace(go.Scatter(x = df['Date'], y=df['Signal_Line'], mode="lines",name='Signal_Line'),
        row = 3, col= 1)
        fig.layout.xaxis.showgrid=False

    # Returns
    if v3=="Daily Returns":
        rets = df['Close'] / df['Close'].shift(1) - 1
        fig.add_trace(go.Scatter(x = df['Date'], y=rets, mode="lines", name = 'Daily Return'),
        row = 4, col= 1,)
        fig.layout.xaxis.showgrid=False
    elif v3=="Cumulative Returns":
        rets = df['Close'] / df['Close'].shift(1) - 1
        cum_rets = (rets + 1).cumprod()
        fig.add_trace(go.Scatter(x = df['Date'], y=cum_rets, mode="lines", name = 'Cumulative Returns'),
        row = 4, col=1)
        fig.layout.xaxis.showgrid=False

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(b=0,t=0,l=0,r=0),plot_bgcolor='#F3F6FA',width=1000, height=600)
    fig.layout.xaxis.showgrid=False
    return fig


app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    
    
    html.Div([    
       
        html.Div([
            html.H1('Dashboard',style={'text-align':'center'}, className = "start"),
            dcc.Dropdown(id="dropdown_tickers", options=[
                {"label":"HDFC Bank Limited", "value":"HDFCBANK.NS"},
                {"label":"ICICI Bank Limited", "value":"ICICIBANK.NS"},
                {"label":"RBL Bank Limited", "value":"RBLBANK.NS"},
                {"label":"Equitas Small Finance Bank Limited", "value":"EQUITASBNK.NS"},
                {"label":"DCB Bank Limited", "value":"DCBBANK.NS"},

                {"label":"Maruti Suzuki India Limited", "value":"MARUTI.NS"},
                {"label":"Tata Motors Limited ", "value":"TATAMOTORS.NS"},
                {"label":"Escorts Limited", "value":"ESCORTS.NS"},
                {"label":"Atul Auto Limited", "value":"ATULAUTO.NS"},

                {"label":"Tata Chemicals Limited", "value":"TATACHEM.NS"},
                {"label":"Pidilite Industries Limited", "value":"PIDILITIND.NS"},
                {"label":"Deepak Nitrite Limited", "value":"DEEPAKNTR.NS"},
                {"label":"Navin Fluorine International Limited", "value":"NAVINFLUOR.NS"},
                {"label":"Valiant Organics Limited", "value":"VALIANTORG.NS"},

                {"label":"Avenue Supermarts Limited ", "value":"DMART.NS"},
                {"label":"Trent Limited", "value":"TRENT.NS"},
                {"label":"V-Mart Retail Limited", "value":"VMART.NS"},
                {"label":"Future Retail Limited", "value":"FRETAIL.NS"},
                {"label":"Shoppers Stop Limited", "value":"SHOPERSTOP.NS"},

                {"label":"Zomato Limited", "value":"ZOMATO.NS"},
                {"label":"G R Infraprojects Limited", "value":"GRINFRA.NS"},
                {"label":"Dodla Dairy Limited", "value":"DODLA.NS"},
                {"label":"India Pesticides Limited ", "value":"IPL.NS"},
                {"label":"Times Green Energy (India) Lim", "value":"TIMESGREEN.BO"},

                {"label":"DLF Limited", "value":"DLF.NS"},
                {"label":"Godrej Properties Limited", "value":"GODREJPROP.NS"},
                {"label":"Oberoi Realty Limited", "value":"OBEROIRLTY.NS"},
                {"label":"Sunteck Realty Limited ", "value":"SUNTECK.NS"},
                {"label":"Nirlon Limited", "value":"NIRLON.BO"},

            ], placeholder='Select Stock',),
            dcc.Dropdown(id="indicators", options=[
                {'label': 'RSI', 'value': 'RSI'},
                {'label': 'SMA', 'value': 'SMA'},
                {'label': 'EMA', 'value': 'EMA'},
                {'label': 'MACD', 'value': 'MACD'}
            ],placeholder='Indicator', ),
            dcc.Dropdown(id="Returns", options=[
                {'label': 'Daily Returns', 'value': 'Daily Returns'},
                {'label': 'Cumulative Returns', 'value': 'Cumulative Returns'},
                # {'label': 'Mean', 'value': 'Mean'},
                # {'label': 'Standard Deviation', 'value': 'Standard Deviation'}
            ],placeholder='Returns', ),
        ]),
    ], className="Navigation"),

    html.Br(),html.Br(),
    html.Div([
        html.Div([
            html.Div([], id="c_graph"), 
            html.Div([], id="graphs"), 
        ], id="main-content")           
    ],className="content")

],className="container")



@app.callback(
            [Output("c_graph", "children")],
            [Output("graphs", "children")],
            [Input("dropdown_tickers", "value")],
            [Input("indicators", "value")],
            [Input("Returns", "value")],
)

def stock_prices(v, v2, v3):
    if v == None:
        raise PreventUpdate

    df = yf.download(v)
    df.reset_index(inplace=True)
    df = df.tail(600)
    MACD(df)
    RSI(df)
    df['SMA'] = SMA(df)
    df['EMA'] = EMA(df)

    fig = get_stock_price_fig(df,v2,v3)
    current = df.iloc[-1][2]
    yesterday = df.iloc[-2][2]

    # Change graph
    fig1 = go.Figure(go.Indicator(
            mode="number+delta",
            value=current,
            delta={'reference': yesterday, 'relative': True,'valueformat':'.2%'}))
    fig1.update_traces(delta_font={'size':15},number_font = {'size':40})
    fig1.update_layout(height=100, margin=dict(b=10,t=20,l=100),)
    if current >= yesterday:
            fig1.update_traces(delta_increasing_color='green')
    elif current < yesterday:
            fig1.update_traces(delta_decreasing_color='red')

    return [dcc.Graph(figure=fig1,config={'displayModeBar': False}),
            dcc.Graph(figure=fig,config={'displayModeBar': False})]


app.run_server(debug=True)