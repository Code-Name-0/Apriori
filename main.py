import pandas as pd
from models.aprio import Aprio
from utils import map_rules, rules_to_json, rules_to_csv, clean_rules
from data.preprocessing.preprocessing import preprocessing

def main(original_ds_path):

    yield "running preprocessing..."
    preprocessing(original_ds_path, './data/transactions.csv', './data/map_stockCode_item.json', 1)

    yield "loading transactions..."
    dataset = pd.read_csv('./data/transactions.csv')

    yield "running apriori algorithm..."
    aprio = Aprio(dataset[:300], 6, 0.2)

    yield "mapping to items and cleanig rules..."
    rules = clean_rules(map_rules(aprio.rules))
    
    yield "writing rules to files..."
    rules_to_json(rules, "./results")
    rules_to_csv(rules, "./results")

if __name__ == "__main__":
    for result in main('./data/original.csv'):
        print(result)
