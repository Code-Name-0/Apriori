from fastapi import FastAPI, File, UploadFile
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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



@app.post("/Predict")
def predict(sample_body: Sample):
    rules_raw = open('../results/rules.json', 'r')
    rules = json.load(rules_raw)

    sets = [rule["antecedent"] for rule in rules ]
    results = []
    sample = sample_body.sample
    for set in sets:
        if len(set) == len(sample):
            for product in sample:
                print(product)
                if (product in set) and not (rules[sets.index(set)] in results):   
                    results.append(rules[sets.index(set)])
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
    



@app.post("/NewDS")
async def create_upload_file(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, size: {file.file._file._st_size} bytes")
    return {"filename": file.filename, "size": file.file._file._st_size}



@app.get("/get_products")
def products():
    products_ = json.load(open('../data/map_stockCode_item.json', 'r'))
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
