from models.aprio import Aprio
from utils import map_rules, rules_to_json, rules_to_markdown, router
from data.preprocessing.preproccessing import preprocessing
import pandas as pd
from data.preprocessing.prepro_utils import remove_missing_description, conv_scode_desc, remove_neg_quan, get_sub_dataset, get_transactions, gen_transactions_csv, map_stock_codes, map_to_json

def main():
    # results = router()
    # code = results["code"]
    # print(results)
    # if code == 3:
    #     print(f"bye!\n")
    #     exit(0)

    # elif code == 2:
    #     dataset_full_path = f"./data/{results['ds_name']}"



    print("running preprocessing...")
    preprocessing('./data/original.xlsx')

    print("loading transactions...")
    dataset = pd.read_csv('./data/transactions.csv')

    print("running apriori algorithm...")
    aprio = Aprio(dataset[:100], 5, 0.5)

    print("mapping to items...")
    rules = map_rules(aprio.rules)

    print("writing to file...")
    rules_to_markdown(rules, "./results")
    rules_to_json(rules, "./results")



if __name__ == "__main__":
    main()