import json
import pandas as pd
import os


def map_rules(rules):
    mapping = open("../map_stockCode_item.json", "r")
    json_map = json.load(mapping)
    
    cp_rules = rules.copy()
    mapped_rules = []
    for rule in cp_rules:
        ant = []
        for item in rule['antecedent']:
            ant.append(json_map[item])

        cons = []
        for item in rule['consequent']:
            cons.append(json_map[item])

        obj = {'antecedent': ', '.join(ant), 'consequent': ', '.join(cons), 'confidence': rule['confidence'], 'lift': rule['lift']}
        mapped_rules.append(obj)

    return mapped_rules

# def map_rules(rules):
#     mapping = open("../map_stockCode_item.json", "r").read()
#     key = '90202A'
#     index = mapping.find(key)
#     for rule in rules:
#         ant = []
#         for item in rule['antecedent']:
#             index = mapping.find(item)
#             text = mapping[index:].split('\n')[0]
#             pattern = r': "(.*?)"'
#             match = re.search(pattern, text)
#             if match:            
#                 ant.append(match.group(1).strip())

#         cons = []
#         for item in rule['consequent']:
#             index = mapping.find(item)
#             text = mapping[index:].split('\n')[0]
#             pattern = r': "(.*?)"'
#             match = re.search(pattern, text) 
#             if match:
#                 cons.append(match.group(1).strip())
           

#         rule['antecedent'] = ant
#         rule['consequent'] = cons

#     return rules

def rules_to_json(rules, path):   

    def filter_fields(dictionary, fields_to_keep):
        return {key: value for key, value in dictionary.items() if key in fields_to_keep}

    filtered_data = [filter_fields(item, ['antecedent', 'consequent', 'lift', 'confidence']) for item in rules]
    file_path = f'{path}/rules.json'
    
    if os.path.exists(file_path):
        with open(f'{path}/rules.json', 'r') as json_file:
            existing_data = json.load(json_file)

        existing_data.extend(filtered_data)
    else:
        existing_data=filtered_data

    existing_data = clean_rules(existing_data)

    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)

    print("successfully wrote results.")

def rules_to_markdown(rules, path):
    with open(f'{path}/rules.md', 'rw') as rules_file:
        line = f"<ol>\n\n"
        for rule in rules:
            line += f"<li>"
            for ant in rule['antecedent'].split(', '):
                line += f"{ant}     "
            
            line += f"========>     "
            for cons in rule['consequent'].split(', '):
                line += f"{cons}          "
            line += f"</li>\n"
        line += f"\n</ol>"
        
        rules_file.write(line)

    print("successfully wrote results.")

def rules_to_csv(rules, path):
        file_path = f"{path}/s6_c02_t3_m30.csv"
        
        if os.path.exists(file_path):
            existing_rules = pd.read_csv(file_path).to_dict('records')
            rules.extend(existing_rules)
            
        rules = clean_rules(rules)
        pd.DataFrame(rules).to_csv(file_path, index=False)



def predict():
    print("predicing")
    pass

def index_matches(rule: dict, rules: list) -> list:
    matching_indexes = []
    for matching_rule in rules:
        if (rule['antecedent'] == matching_rule['antecedent']) \
            and (rule['consequent'] == matching_rule['consequent']):
            matching_indexes.append(rules.index(matching_rule))
    max = 0
    for i in matching_indexes:
        if rules[i]['lift'] > max:
            max = rules[i]['lift']
            highest_lift_index = i
    matching_indexes.remove(highest_lift_index)
    return matching_indexes

def clean_rules(rules: list) -> None:
   
    for rule in rules:
        array_matched_rules = index_matches(rule=rule, rules=rules) 
        if array_matched_rules:
            for index in array_matched_rules:
                rules.pop(index)
        elif len(rule['consequent']) == 0:
            rules.remove(rule)
        # TODO: add the code to save the reuslt to the file
    return rules