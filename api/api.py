import io
import pandas as pd
import json
from main import main
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, UploadFile, File

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Body(BaseModel):
    name: str

class Sample(BaseModel):
    sample: list



@app.get("/dummy_get")
def hello(name: str):
  return {"Hello " + name + ", Free Palestine! 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸"}

@app.post("/dummy_post")
def send_here(body: Body):
   return {"Hello " + body.name + ", Free Palestine! 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸"}

@app.post("/Predict")
def predict(sample_body: Sample):

    rules_raw = open('./results/rules.json', 'r')
    rules = json.load(rules_raw)

    sets = [rule["antecedent"].split(', ') for rule in rules ]

    results = []

    sample = sample_body.sample
    
    for set in sets:
        if len(set) == len(sample):
            for product in sample:
                if (product in set) and not (rules[sets.index(set)] in results):   
                    results.append(rules[sets.index(set)])

    return results

@app.websocket("/train_websocket")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        for status in main( "./data/original.csv"):
            await websocket.send_text(status)

        await websocket.send_text("new rules are available")
        await websocket.close()

    except Exception as e:
        print("Error:", repr(e))

@app.post("/NewDS")
async def newDS( file: UploadFile = File(...) ):
    try:
        contents = await file.read()

        df = pd.read_csv(io.StringIO(contents.decode('utf-8')), index_col=0)

        valid = True
        required_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
        'UnitPrice', 'CustomerID', 'Country']
        problems = []

        # Check if all required columns are in the DataFrame
        for column in required_columns:
            if column not in df.columns:
                problems.append(column)

        # Check if the DataFrame has any extra columns
        for column in df.columns:
            if column not in required_columns:
                problems.append(column)
        
        if len(problems) != 0:
            raise Exception("the provided dataset is not accepted")
        
        print('writing df to csv')
        path = './data/original.csv'
        df.to_csv(path)

        return {"valid": valid, "problems": problems}

    except Exception as e:
       return {"status": "failure", "message": e, "extra": problems}

@app.get("/get_products")
def products():

    products_ = json.load(open('./data/map_stockCode_item.json', 'r'))
    products = []

    for p in products_.keys():
        if not (products_[p] in products):
            products.append(products_[p])

    return products
