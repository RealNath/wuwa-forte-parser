import json

def get_string(id, multitext):
    try:
        return multitext[id]['Content']
    except KeyError:
        return