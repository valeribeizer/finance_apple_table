import  os
import yfinance as yf
import pymongo
import json
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

#date range
start = datetime.datetime(2021,6,30)
end = datetime.datetime(2021,8,1)

#get  data from Yahoo finance
apple = yf.download('AAPL', start=start, end=end)
apple.reset_index(drop=False, inplace=True)
apple.rename_axis(None)
apple['Date'] = apple['Date'].dt.strftime('%Y-%m-%d')


app = FastAPI()
# app.config['MONGODB_SETTINGS'] = {
#     'host': os.environ['MONGODB_HOST'],
#     'username': os.environ['MONGODB_USERNAME'],
#     'password': os.environ['MONGODB_PASSWORD'],
#     'db': 'apple_stocks'
# }

class Stocks(BaseModel):
    date: str = Field(alias='Date')
    open: float = Field(alias='Open')
    high: float = Field(alias='High')
    low: float = Field(alias='Low')
    close: float = Field(alias='Close')
    adj_close: float = Field(alias='Adj Close')
    volume: int = Field(alias='Volume')

#connection to MongoDB
client = pymongo.MongoClient("mongodb+srv://valeryiabeizer:pCV32dYi94mAS@cluster0.y2ttp.mongodb.net/apple_stocks?retryWrites=true&w=majority")

#creating db    
db = client['apple_stocks']
collection = db['prices']

#sending data to db
for index, row in apple.iterrows():
    apple_data = json.loads(apple.loc[index].to_json(orient='index'))
    collection.update_many(apple_data, {"$set":apple_data}, upsert=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def list_stocks():
    stocks_info = []
    for stocks in collection.find({}, {"_id":0}):
        stocks_info.append(Stocks(**stocks))
    return stocks_info


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)