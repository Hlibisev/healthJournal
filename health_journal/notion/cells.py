def date_cell(date):
    return {"date": {"start": date}}

def text_cell(text):
    return {"rich_text": [{"text": {"content": text}}]}

def title_cell(text):
    return {"title": [{"text": {"content": text}}]}

def number_cell(number):
    return {"number": number}

def rich_text_cell(text):
    return {"rich_text": [{"text": {"content": text}}]}

def select_cell(text):
    return {"select": {"name": text}}

cells = {
    "date": date_cell,
    "text": text_cell,
    "title": title_cell,
    "number": number_cell,
    "rich_text": text_cell,
    "select": select_cell,
}