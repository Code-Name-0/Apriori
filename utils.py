import json
import re

def map_rules(rules):
    mapping = open("../map_stockCode_item.json", "r").read()
    key = '90202A'
    index = mapping.find(key)
    for rule in rules:
        ant = []
        for item in rule['antecedent']:
            index = mapping.find(item)
            text = mapping[index:].split('\n')[0]
            pattern = r': "(.*?)"'
            match = re.search(pattern, text)
            if match:            
                ant.append(match.group(1).strip())

        cons = []
        for item in rule['consequent']:
            index = mapping.find(item)
            text = mapping[index:].split('\n')[0]
            pattern = r': "(.*?)"'
            match = re.search(pattern, text) 
            if match:
                cons.append(match.group(1).strip())
           

        rule['antecedent'] = ant
        rule['consequent'] = cons

    return rules

def rules_to_json(rules, path):   

    def filter_fields(dictionary, fields_to_keep):
        return {key: value for key, value in dictionary.items() if key in fields_to_keep}

    filtered_data = [filter_fields(item, ['antecedent', 'consequent', 'lift', 'confidence']) for item in rules]

    json_data = json.dumps(filtered_data, indent=2)
    with open(f'{path}/rules.json', 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
        print("successfully wrote results.")
    

def rules_to_markdown(rules, path):
    rules_file = open(f'{path}/rules.md', 'w')
    line = f"<ol>\n"
    for rule in rules:
        line += f"<li>"
        for ant in rule['antecedent']:
            line += f"{ant}     "
        
        line += f"========>     "
        for cons in rule['consequent']:
            line += f"{cons}          "
        line += f"</li>\n"
    line += f"</ol>"
    rules_file.write(line)

    rules_file.close()

def predict():
    print("predicing")
    pass

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




"""
    {'antecedent': ['22555'],
  'consequent': ['22556'],
  'confidence': 0.7142857142857143,
  'lift': 11.904761904761905}
"""
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


def clean_rules_json(path: str) -> None:
    with open(path, 'r') as rules_json_file:
        rules = list(json.load(rules_json_file))
        for rule in rules:
            array_matched_rules = index_matches(rule=rule, rules=rules) 
            if array_matched_rules:
                for index in array_matched_rules:
                    rules.pop(index)
            elif len(rule['consequent']) == 0:
                rules.remove(rule)
        # TODO: add the code to save the reuslt to the file
        return rules