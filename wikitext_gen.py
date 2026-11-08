import json
import re
from get_string import get_string

with open('MultiText.json', 'r', encoding='utf-8') as f:
    multitext = json.load(f)

with open('skilldescription.json', 'r', encoding='utf-8') as f:
    skilldescription = json.load(f)

with open('skill.json', 'r', encoding='utf-8') as f:
    skill = json.load(f)

with open('termconfig.json', 'r', encoding='utf-8') as f:
    termconfig = json.load(f)

def are_all_same(list):
    return list.count(list[0]) == len(list)

def get_skills(character_id):
    return [
        skill_id for skill_id, data in skill.items()
        if data.get('SkillGroupId') == character_id
    ]

def get_skill_attributes(skill_id):
    attrs = [
        attr for attr in skilldescription.values()
        if attr.get('SkillLevelGroupId') == int(skill_id)
    ]
    return sorted(attrs, key=lambda x: x.get('Order', 0))

def get_skill_attr_stats(skill_attr, min_level = 1, max_level = 10):
    if skill_attr and skill_attr.get('SkillDetailNum'):
        stats = skill_attr['SkillDetailNum'][0]['ArrayString']
        if are_all_same(stats): return stats[0]
        return ';'.join(stats[(min_level-1):max_level])

def parse_saptag(text):
    values = {}
    def unwrap(m):
        values[m.group(1)] = m.group(2)
        return m.group(2)
    text = re.sub(r"<SapTag=(\d+)>(.*?)</SapTag>", unwrap, text, flags=re.S)

    def choose(m):
        singular, plural, tag = m.group(1), m.group(2), m.group(3)
        value = re.sub(r"<[^>]*>", "", values.get(tag, "")).strip().replace(",", "")
        try:
            return singular if float(value) <= 1 else plural
        except ValueError:
            return plural
    return re.sub(r"\{Cus:Sap,S=(.*?) P=(.*?) SapTag=(\d+)\}", choose, text)

def parse_cus_ipt(text):
    def tooltip(m):
        touch, pc, gamepad = m.group(1), m.group(2), m.group(3)
        return f"({{{{Tt|{touch}|Touch}}}}/{{{{Tt|{pc}|PC}}}}/{{{{Tt|{gamepad}|Gamepad}}}})"
    return re.sub(r"\{Cus:Ipt,Touch=(.*?) PC=(.*?) Gamepad=(.*?)\}", tooltip, text)

def format_text(text):
    text = re.sub(
        r"<color=(Highlight|Title)>\s*<te href=(.*?)>(.*?)</te>\s*</color>",
        lambda m: (
            f"<te href={m.group(2)}>"
            f"{{{{Color|{'help' if m.group(1) == 'Highlight' else 'menu'}"
            f"|{m.group(3)}|nobold=1}}}}</te>"
        ),
        text, flags=re.S)
    text = parse_saptag(text)
    text = parse_cus_ipt(text)
    text = re.sub(r"</?size(=(.*?))?>", "", text)
    # text = re.sub(r"\s*\{Cus:[^}]*\}", "", text)
    text = text.replace("\n", "<br><!--\n-->").replace("<br><!--\n--><br><!--\n-->", "<br><br><!--\n\n-->")
    text = re.sub(r"<color=Title>(.*?)</color>", r"{{Color|menu|\1}}", text, flags=re.S)
    text = re.sub(r"<color=Highlight>(.*?)</color>", r"{{Color|help|\1|nobold=1}}", text, flags=re.S)
    text = text.replace(
        "<color=Wind>Aero DMG</color>", "{{Color|Aero DMG|nobold=1}}").replace(
        "<color=Light>Spectro DMG</color>", "{{Color|Spectro DMG|nobold=1}}").replace(
        "<color=Fire>Fusion DMG</color>", "{{Color|Fusion DMG|nobold=1}}").replace(
        "<color=Thunder>Electro DMG</color>", "{{Color|Electro DMG|nobold=1}}").replace(
        "<color=Ice>Glacio DMG</color>", "{{Color|Glacio DMG|nobold=1}}").replace(
        "<color=Dark>Havoc DMG</color>", "{{Color|Havoc DMG|nobold=1}}")
    return text

def fill_placeholders(text, values):
    if not values: return text
    def replace(m):
        i = int(m.group(1))
        if i >= len(values): return m.group(0)
        value = str(values[i])
        # Prevent double percent signs
        if value.endswith("%") and m.string[m.end():m.end() + 1] == "%":
            value = value[:-1]
        return value
    return re.sub(r"\{(\d+)\}", replace, text)

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
            # Reuse needs the title as well: the template looks the stored
            # description up by {{{2|{{{1}}}}}}, not by the styled display text.
            return f"{{{{Extra Effect|{text}|{title}}}}}" if title else f"{{{{Extra Effect|{text}}}}}"
        seen_te.add((href, text))
        term_desc = get_string(f"Term{href}_Desc", multitext) or ""
        term_desc = fill_placeholders(term_desc, termconfig.get(href, {}).get('Placeholder', []))
        term_desc = format_text(term_desc)
        return f"{{{{Extra Effect|{text}|{title}|{term_desc}}}}}"

    return re.sub(r"<te href=(.*?)>(.*?)</te>", replace_te, desc)

def main():
    skill_ids = get_skills(1312)
    print(f"Skill IDs: {skill_ids}")

    for skill_id in skill_ids:
        skill_name = get_string(skill[skill_id]['SkillName'], multitext)
        print(f"{skill_name}")

        skill_attributes = get_skill_attributes(skill_id)
        if skill_attributes:
            print(get_skill_description(skill_id))

            skill_type = skill[skill_id]['SkillType']
            talent_type = get_string(f"SkillType_{skill_type}_TypeName", multitext)
            levels = skill[skill_id].get('MaxSkillLevel', 10)
            attr_names = [get_string(attr['AttributeName'], multitext) for attr in skill_attributes]
            order_and_titles = ', '.join(attr_names)

            print("\n==Attribute Scaling==")
            print("{{Skill Scaling")
            print(f"|talentType = {talent_type}")
            print(f"|levels = {levels}")
            print(f"|order = {order_and_titles}")
            print(f"|titles = {order_and_titles}\n")

            for skill_attr, attr_name in zip(skill_attributes, attr_names):
                skill_attr_stats = get_skill_attr_stats(skill_attr)
                print(f"|{attr_name} = {skill_attr_stats}")
            print("}}\n")

main()
