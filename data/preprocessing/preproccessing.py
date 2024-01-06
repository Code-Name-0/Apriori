import pandas as pd
from data.preprocessing.prepro_utils import remove_missing_description, conv_scode_desc, remove_neg_quan, get_sub_dataset, get_transactions, gen_transactions_csv, map_stock_codes, map_to_json

def preprocessing(original_dataset_path):
    original = pd.read_excel(f'{original_dataset_path}')

    remove_missing_description(dataset=original)
    conv_scode_desc(original)
    remove_neg_quan(original)
    subset = get_sub_dataset(original, ['InvoiceNo', 'Quantity', 'UnitPrice', 'Country'])
    transactions = get_transactions(subset, 3)
    gen_transactions_csv(transactions,'..')

    mapping = map_stock_codes(subset)
    map_to_json(mapping, '..')
    print("finished prepro")
