import json
import re

def map_rules(rules):
    mapping = open("../map_stockCode_item.json", "r").read()
    key = '90202A'
    index = mapping.find(key)
    #print(mapping[index:].split('\n')[0].split(': ')[1][:-1])
    for rule in rules:
        ant = []
        for item in rule['antecedent']:
            index = mapping.find(item)
            text = mapping[index:].split('\n')[0]
            pattern = r': "(.*?)"'
            match = re.search(pattern, text)
            if match:            
                ant.append(match.group(1))

        cons = []
        for item in rule['consequent']:
            index = mapping.find(item)
            text = mapping[index:].split('\n')[0]
            pattern = r': "(.*?)"'
            match = re.search(pattern, text) 
            if match:
                cons.append(match.group(1))
           

        rule['antecedent'] = ant
        rule['consequent'] = cons

    return rules

def rules_to_json(rules, path):   

    def filter_fields(dictionary, fields_to_keep):
        return {key: value for key, value in dictionary.items() if key in fields_to_keep}

    filtered_data = [filter_fields(item, ['antecedent', 'consequent', 'lift', 'confidence']) for item in rules]

    json_data = json.dumps(filtered_data, indent=2)
    try:
        with open(f'{path}/rules.json', 'w') as json_file:
            json_file.write(json_data)
            json_file.close()
        print("successfully wrote results.")
    except Exception as e:
        print(f"Error writing the file: {e}")

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

"""
    {'antecedent': ['22555'],
  'consequent': ['22556'],
  'confidence': 0.7142857142857143,
  'lift': 11.904761904761905}
"""
