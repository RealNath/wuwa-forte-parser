from utils import (
    get_string,
    get_skill_attributes,
    get_skill_attr_stats,
    get_skill_description,
    get_skills,
    multitext,
    skill,
)

# SKILLTYPE_NUM_NO_LEVEL = [4, 7, 8, 9, 10] # Inherent Skill
ACTIVE_SKILLTYPE_NUM = [1, 2, 3] # Normal Attack, Resonance Skill, Resonance Liberation
PASSIVE_SKILLTYPE_NUM = [4, 6, 7, 8, 9, 10] # Forte Circuit, Inherent Skill
CONCERTO_SKILLTYPE_NUM = [5, 11] # Intro Skill, Outro Skill

def main():
    character_id = 1312
    skill_ids = get_skills(character_id)
    # print(f"Skill IDs: {skill_ids}")

    wikitext = []
    for skill_id in skill_ids:
        skill_name = get_string(skill[skill_id]['SkillName'], multitext)
        wikitext.append(f"\n\n{skill_name}")
        # print(skill_id)
        wikitext.append(f"{{{{Skill Infobox")
        wikitext.append(f"|image         = Skill {skill_name.replace(':','')}.png")
        
        character_name = get_string(f'RoleInfo_{character_id}_Name', multitext)
        wikitext.append(f"|resonator     = {character_name}")
        
        skill_type_num = skill[skill_id]['SkillType']
        skill_type = get_string(f"SkillType_{skill_type_num}_TypeName", multitext)
        wikitext.append(f"|type          = {skill_type}")

        if (skill_type_num in ACTIVE_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Active Skills")
        elif (skill_type_num in PASSIVE_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Passive Skills")
        elif (skill_type_num in CONCERTO_SKILLTYPE_NUM):
            wikitext.append(f"|type2         = Concerto Skills")
        
        wikitext.append(f"|info          = {get_skill_description(skill_id)}")

        skill_attributes = get_skill_attributes(skill_id)
        if skill_attributes and skill_id.get('MaxSkillLevel', 10) > 1:
            levels = skill[skill_id].get('MaxSkillLevel', 10)
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
        wikitext.append("}}\n")

        print("\n".join(wikitext))

main()
