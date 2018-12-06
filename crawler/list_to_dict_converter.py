import json
from typing import Dict, List

if __name__ == '__main__':
    with open('description_final.json', 'r', encoding='utf-8') as descriptions_file:
        descriptions_list: List[Dict[str, str]] = json.load(descriptions_file)

    descriptions_dict: Dict[str, str] = dict()

    for complex_description in descriptions_list:
        offer, description = complex_description.popitem()
        better_offer = offer.replace('-N-', '-')
        descriptions_dict[better_offer] = description

    with open('description_dict.json', 'w') as new_descriptions_file:
        json.dump(descriptions_dict, new_descriptions_file)
