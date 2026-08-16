from settings import *

history = {}

def load_history():
    with open(history_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        history.clear()
        history.update({int(k) if k.isdigit() else k: v for k, v in data.items()})


def save_history():
    with open(history_file_path, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent= 4)
    
def add_to_history(text, from_id, to_id, date):
    if from_id in history:
        history[from_id].append([to_id, text, date])
    else:
        history[from_id] = []
        history[from_id].append([to_id, text, date])

    save_history()


