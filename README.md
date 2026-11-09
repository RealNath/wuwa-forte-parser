# Wuthering Waves Forte Parser

This is a program that helps you automatically parse and generate wikitext for each Resonator's fortes (for Wuthering Waves wiki).

## How to use

1. Clone this repo, or download it as a zip.
    ```bash
    git clone https://github.com/RealNath/wuwa-forte-parser
    cd src
    ```

2. Download the needed files from the [arikatsu](https://github.com/Arikatsu/WutheringWaves_Data) repo, and adjust the json structure for this program:
    ```bash
    python download_json.py {game_version} {language}
    python optimize_json.py
    ```
    For example: `python download_json.py 3.7 en`  
    Leave out `game_version` and `language` to download the latest English MultiText.  
    This consists of the following files:
    - `BinData/skill/skill.json`
    - `BinData/skill/skilldescription.json`
    - `BinData/skillTree/skilltree.json`
    - `BinData/Term/termconfig.json`
    - `Textmaps/{lang}/multi_text/MultiText.json`

3. Run this command:
    ```bash
    python wikitext_gen.py {CharacterID}
    ```
    * `CharacterId` can be found at MultiText.json, by searching `"Content": "{character name}",` then find the JSON key (previous line) that is `RoleInfo_{CharacterID}_Name`
    
    For example: `python wikitext_gen.py 1312` (Suoming)

4. See the `../output/` folder. The wikitext files will be generated with the name of the forte, ending with `.wikitext` extension.