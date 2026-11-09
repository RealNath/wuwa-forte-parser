import pathlib
from utils import (
    get_string,
    get_skill_attributes,
    get_skill_attr_stats,
    get_skill_description,
    get_inherent_skill_label,
    get_skills,
    multitext,
    skill
)

OUTPUT_DIR = pathlib.Path(__file__).parent / ".." / "output"
# SKILLTYPE_NUM_NO_LEVEL = [4, 7, 8, 9, 10] # Inherent Skill
ACTIVE_SKILLTYPE_NUM = [1, 2, 3] # Normal Attack, Resonance Skill, Resonance Liberation
INHERENT_SKILLTYPE_NUM = [4, 7, 8, 9, 10] # Inherent Skill
PASSIVE_SKILLTYPE_NUM = [6] + INHERENT_SKILLTYPE_NUM # Forte Circuit, Inherent Skill
INTRO_SKILLTYPE_NUM = [5] # Intro Skill
OUTRO_SKILLTYPE_NUM = [11] # Outro Skill
CONCERTO_SKILLTYPE_NUM = INTRO_SKILLTYPE_NUM + OUTRO_SKILLTYPE_NUM

def main():
    character_id = 1312
    skill_ids = get_skills(character_id)
    # print(f"Skill IDs: {skill_ids}")

    for skill_id in skill_ids:
        wikitext = []
        skill_data = skill[skill_id]
        skill_name = get_string(skill_data['SkillName'], multitext)
        # wikitext.append(f"{skill_name}")
        # wikitext.append(skill_id)
        wikitext.append(f"{{{{Skill Infobox")
        wikitext.append(f"|image         = Skill {skill_name.replace(':','')}.png")
        
        character_name = get_string(f'RoleInfo_{character_id}_Name', multitext)
        wikitext.append(f"|resonator     = {character_name}")
        
        skill_type_num = skill_data['SkillType']
        skill_type = get_string(f"SkillType_{skill_type_num}_TypeName", multitext)
        wikitext.append(f"|type          = {skill_type}")

        if (skill_type_num in ACTIVE_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Active Skills")
        elif (skill_type_num in PASSIVE_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Passive Skills")
            if (skill_type_num in INHERENT_SKILLTYPE_NUM):
                type3 = get_inherent_skill_label(character_id, skill_id, INHERENT_SKILLTYPE_NUM)
                wikitext.append(f"|type3         = {type3}")
        elif (skill_type_num in CONCERTO_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Concerto Skills")
        
        wikitext.append(f"|info          = {get_skill_description(skill_id)}")
        wikitext.append("}}")
        wikitext.append("{{Intro/Skill}}")

        skill_attributes = get_skill_attributes(skill_id)
        if skill_attributes and skill_data.get('MaxSkillLevel', 10) > 1:
            levels = skill_data.get('MaxSkillLevel', 10)
            attr_names = [get_string(attr['AttributeName'], multitext) for attr in skill_attributes]
            order_and_titles = ', '.join(attr_names)

            wikitext.append("\n==Attribute Scaling==")
            wikitext.append("{{Skill Scaling")
            wikitext.append(f"|talentType = {skill_type}")
            wikitext.append(f"|levels = {levels}")
            wikitext.append(f"|order = {order_and_titles}")
            wikitext.append(f"|titles = {order_and_titles}\n")

            for skill_attr, attr_name in zip(skill_attributes, attr_names):
                skill_attr_stats = get_skill_attr_stats(skill_attr)
                wikitext.append(f"|{attr_name} = {skill_attr_stats}")
            wikitext.append("}}")

        if (skill_type_num in INHERENT_SKILLTYPE_NUM):
            wikitext.append("\n==Skill Upgrade==")
            wikitext.append(f"{{{{Skill Upgrade|{character_name}|inherentSkill}}}}")
        elif (skill_type_num not in OUTRO_SKILLTYPE_NUM):
            wikitext.append("\n==Skill Upgrade==")
            wikitext.append(f"{{{{Skill Upgrade|{character_name}|mainForte}}}}")
        
        wikitext.append("\n==Other Languages==")
        wikitext.append("(soon)")

        wikitext.append("\n==Change History==")
        wikitext.append("{{Change History|X.X}}")
        
        wikitext.append("\n==Navigation==")
        wikitext.append(f"{{{{Skill Navbox|{character_name}}}}}")

        # print("\n".join(wikitext))
        with open(OUTPUT_DIR / f"{skill_name}.wikitext", "w") as f:
            f.write("\n".join(wikitext))

main()
