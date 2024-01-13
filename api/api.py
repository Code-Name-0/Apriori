from fastapi import FastAPI, WebSocket, UploadFile, File
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
from main import main
from data.preprocessing import preproccessing
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

class NewDS(BaseModel):
    dataset: UploadFile = File(...)

@app.get("/dummy_get")
def hello(name: str):
  return {"Hello " + name + ", Free Palestine! 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸"}


@app.post("/dummy_post")
def send_here(body: Body):
   return {"Hello " + body.name + ", Free Palestine! 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸"}


import pandas as pd
@app.post("/Predict")
def predict(sample_body: Sample):
    rules_raw = open('./results/rules.json', 'r')
    rules = json.load(rules_raw)

    sets = [rule["antecedent"].split(', ') for rule in rules ]
    results = []
    sample = sample_body.sample
    
    for set in sets:
        # if len(set) == 1:
        #     print(len(set))
        if len(set) == len(sample):
            for product in sample:
                # print(product)
                if (product in set) and not (rules[sets.index(set)] in results):   
                    results.append(rules[sets.index(set)])
    print(results)
    return results


def train():
    ds_name = str(input(f"place the dataset inside the data folder and provide its name\n$>"))
    num_samples = int(input(f"how many sample you want to use (0 for full dataset)?\n$>"))
    return {"code": 2, "ds_name": ds_name, "num_samples": num_samples}


def quit_():
    return {"code": 3}

def router():
    choice = int(input(f"1 - predict\n2 - train\n3 - Quit\n$>"))
    choices = {1: predict, 2: train, 3: quit_()}

    
    if choice in choices.keys():
        return choices[choice]()
    else:
        return {"code": -1}
    
import asyncio



processing_status = {}
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
            #TODO: convert the file into pd.DataFrame
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')), index_col=0)

        #TODO: check columns 

        c = 0
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
        
        #TODO: execute preprocessing and rules generation
        # save the dataset as /data/original.csv
        path = './data/original.csv'
        print('writing df to csv')
        # processing_status[client_id] = "writing df to csv"
        df.to_csv(path)
        # print('')
        
        # # processing_status["status"] = "running main"
        # main(path)

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


"""
    {'antecedent': ['22555'],
  'consequent': ['22556'],
  'confidence': 0.7142857142857143,
  'lift': 11.904761904761905}
"""
