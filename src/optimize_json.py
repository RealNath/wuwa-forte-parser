import json
import pathlib

DATA_DIR = pathlib.Path(__file__).parent / ".." / "data"

# convert from list of dict to dict
# (key: value of a given `key`, value: the rest of key-value pairs)
def optimize_json(json_file, key):
    with open(DATA_DIR / json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = {}
    for item in data:
        item_id = item.pop(key)
        if item_id not in result:
            result[item_id] = item
        elif isinstance(result[item_id], list):
            result[item_id].append(item)
        else:
            result[item_id] = [result[item_id], item]

    with open(f"{json_file.replace('.json', '')}.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

# optimize_json('MultiText.json', 'Id')
# optimize_json('achievement.json', 'Id')
# optimize_json('achievementcategory.json', 'Id')
# optimize_json('achievementgroup.json', 'Id')
# optimize_json('achievementstarlevel.json', 'Level')
optimize_json('skill.json', 'SkillGroupId')
optimize_json('skilldescription.json', 'SkillLevelGroupId')
optimize_json('termconfig.json', 'Id')