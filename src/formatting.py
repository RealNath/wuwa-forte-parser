import re

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
