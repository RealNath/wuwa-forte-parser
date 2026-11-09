import json
from pathlib import Path
import re
import json

from formatting import format_text, fill_placeholders

DATA_DIR = Path(__file__).parent / ".." / "data"
MIN_LEVEL = 1
MAX_LEVEL = 10

with open(DATA_DIR / 'MultiText.json', 'r', encoding='utf-8') as f:
    multitext = json.load(f)

with open(DATA_DIR / 'skilldescription.json', 'r', encoding='utf-8') as f:
    skilldescription = json.load(f)

with open(DATA_DIR / 'skill.json', 'r', encoding='utf-8') as f:
    skill = json.load(f)

with open(DATA_DIR / 'termconfig.json', 'r', encoding='utf-8') as f:
    termconfig = json.load(f)

with open(DATA_DIR / 'skilltree.json', 'r', encoding='utf-8') as f:
    skilltree = json.load(f)

def get_string(id, multitext):
    try:
        return multitext[id]['Content']
    except KeyError:
        return

def are_all_same(list):
    return list.count(list[0]) == len(list)

def get_skills(character_id):
    return [
        skill_id for skill_id, data in skill.items()
        if data.get('SkillGroupId') == character_id
    ]

def get_inherent_skill_label(character_id, skill_id, inherent_skill_types):
    nodes = skilltree.get(str(character_id), [])
    node_data = next((node for node in nodes if str(
                        node.get('SkillId')) == str(skill_id)
                    ), None)
    if node_data:
        parent_nodes = node_data.get('ParentNodes', [])
        for node in nodes:
            if node.get('NodeIndex') in parent_nodes:
                previous_skill_id = skill.get(str(node.get('SkillId')), {})
                if previous_skill_id.get('SkillType') in inherent_skill_types:
                    return "2nd Inherent Skills"
    return "1st Inherent Skills"

def get_skill_attributes(skill_id):
    attrs = [
        attr for attr in skilldescription.values()
        if attr.get('SkillLevelGroupId') == int(skill_id)
    ]
    return sorted(attrs, key=lambda x: x.get('Order', 0))

def get_skill_attr_stats(skill_attr, min_level = MIN_LEVEL, max_level = MAX_LEVEL):
    if skill_attr and skill_attr.get('SkillDetailNum'):
        stats = skill_attr['SkillDetailNum'][0]['ArrayString']
        if are_all_same(stats): return stats[0]
        return ';'.join(stats[(min_level-1):max_level])

def get_skill_description(skill_id):
    raw = get_string(f"Skill_{skill_id}_SkillDescribe", multitext)
    if not raw: return ""

    skill_detail_num = skill.get(str(skill_id), {}).get('SkillDetailNum', [])
    
    desc = format_text(fill_placeholders(raw, skill_detail_num))

    seen_te = set()
    def replace_te(m):
        href = m.group(1).strip("\"'")
        text = m.group(2)
        title = get_string(f"Term{href}_Title", multitext) or ""
        if (href, text) in seen_te:
            return f"{{{{Extra Effect|{text}|{title}}}}}" if title else f"{{{{Extra Effect|{text}}}}}"
        seen_te.add((href, text))
        term_desc = get_string(f"Term{href}_Desc", multitext) or ""
        term_desc = fill_placeholders(term_desc, termconfig.get(href, {}).get('Placeholder', []))
        term_desc = format_text(term_desc)
        return f"{{{{Extra Effect|{text}|{title}|{term_desc}}}}}"

    return re.sub(r"<te href=(.*?)>(.*?)</te>", replace_te, desc)
