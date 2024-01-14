import pandas as pd
from models.aprio import Aprio
from utils import map_rules, rules_to_json, rules_to_markdown, clean_rules
from data.preprocessing import preprocessing
from data.preprocessing.prepro_utils import remove_missing_description, conv_scode_desc, remove_neg_quan, get_sub_dataset, get_transactions, gen_transactions_csv, map_stock_codes, map_to_json


def main(original_ds_path):

    yield "running preprocessing..."
    preprocessing(original_ds_path, './data/transactions.csv', './data/map_stockCode_item.json', 1)

    yield "loading transactions..."
    dataset = pd.read_csv('./data/transactions.csv')

    yield "running apriori algorithm..."
    aprio = Aprio(dataset[:500], 5, 0.4)

    yield "mapping to items and cleanig rules..."
    rules = clean_rules(map_rules(aprio.rules))
    
    yield "writing to file..."
    rules_to_markdown(rules, "./results")
    rules_to_json(rules, "./results")

if __name__ == "__main__":
    for result in main('./data/original.csv'):
        
        print(result)
