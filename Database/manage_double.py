import json

def remove_duplicates(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    unique_data = []
    seen = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if item_json not in seen:
            unique_data.append(item)
            seen.add(item_json)

    with open('unique_' + json_file, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, indent=2, ensure_ascii=False)

remove_duplicates("db.json")