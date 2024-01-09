import json
import pandas as pd


def remove_neg_quan(dataset):
    dataset["Quantity"] = dataset[dataset["Quantity"] > 0]["Quantity"]

def remove_missing_description(dataset):
    dataset.dropna(subset=['Description'], inplace=True)

def conv_scode_desc(dataset):
    dataset["StockCode"] = dataset["StockCode"].apply(lambda x: str(x))
    dataset["Description"] = dataset["Description"].apply(lambda x: str(x))

def get_sub_dataset(dataset, columns_to_remove):
    return dataset.drop(columns=columns_to_remove)

def get_transactions(dataset, time_interval):
    transactions = []
    for _, customer_ in dataset.groupby('CustomerID'):

        transaction = []
        reference_time = None

        for _, row in customer_.iterrows():
            time = str(row['InvoiceDate']).split(' ')[1]
            hour = int(time[:2])
            minute = int(time[3:5])
    
            if reference_time is None:
                reference_time = {"h": hour, "m": minute}

            if hour == reference_time['h'] and abs(minute - reference_time['m']) <= time_interval:
                if len(transaction) == 30:
                    transactions.append(transaction)
                    transaction = [row['StockCode']]
                    reference_time = {"h": hour, "m": minute}
                else:
                    transaction.append(row['StockCode'])

            else:
                transactions.append(transaction)
                transaction = [row['StockCode']]
                reference_time = {"h": hour, "m": minute}

        transactions.append(transaction)
    return transactions

def gen_transactions_csv(transactions, path):
    apriory_df = pd.DataFrame(transactions)
    apriory_df.to_csv(f'{path}', index=False)
    print('writen to',f'{path}')


def map_stock_codes(dataset):
    mapping = []
    for code, row in dataset.groupby('StockCode'):
        mapping.append([code, row["Description"].iloc[0].strip()])

    return mapping


def map_to_json(mapping, path):
    mapping_dict = {code: item for code, item in mapping}
    json_result = json.dumps(mapping_dict, indent=2)
    json_file = open(f'{path}', 'w')
    json_file.write(json_result)
    json_file.close()

