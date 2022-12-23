from fastapi import FastAPI, Query
import os
from typing import List
from model import textNotes, infoNotes, listNotes, createNotes
import json
from datetime import datetime


app = FastAPI()
def print_token():
    with open('token.txt', 'r') as file:
        id = file.read()
    return id

def filter():
    files = os.listdir(r'C:\Users\Evgeniy\PycharmProjects\LabaAPI')
    result = [0]
    ext = '.json'
    for filename in files:
        if filename.endswith(ext):
            filename = filename.replace('.json', '')
            result.append(filename)
    result = list(map(int, result))
    return sorted(result)


def create():
    files = filter()
    print(files)
    name = files[len(files) - 1] + 1
    print(files[len(files) - 1])
    with open(str(name) + '.json', 'w') as file:
        a = textNotes(id= name, text = '')
        b = infoNotes(creat = datetime.now(), updated = datetime.now())
        b = {k: str(v) for k, v in b.dict().items()}
        c = {
            'note' : a.dict(),
            'data' : b
        }
        json.dump(c, file)

    return name
@app.post('/createnote')
def createNote(id:textNotes,token: str = Query(...,)):
    if token == print_token():
        id = create()
        return id
    else:
        return 'createERROR'

@app.get('/getnote')
def getNote(token: str, id:int):
    if token == print_token():
        with open(str(id)+".json", "r") as file:
            notes = json.load(file)
        note = notes['note']
        a = textNotes(id = note['id'], text = note['text'])
        return a
    else:
        return 'createERROR'

@app.patch('/updatenote')
def updateNote(token: str, id:int, text:str):
    if token == print_token():
        with open(str(id)+".json", "r") as file:
            notes = json.load(file)
        notes['note']['text'] = text
        notes['data']['updated'] = str(datetime.now())
        with open(str(id)+".json", "w") as file:
            json.dump(notes, file)
        note = notes['note']
        a = textNotes(id=note['id'], text=note['text'])
        return a
    else:
        return 'createERROR'

@app.delete('/delete_note')
def delete_note(token: str, id:int):
    if token == print_token():
        path = r'C:\Users\Evgeniy\PycharmProjects\Lab4'+f'\{str(id)}.json'
        try:
            os.remove(path)
            return f'Заметка {id} удалена'
        except:
            return 'Заметки с таким id не найдено'
    else:
        return 'createERROR'

@app.get('/list_note')
def list_note(token: str):
    if token == print_token():
        n_list : List[int] = list(map(int,filter()))
        n_list.remove(0)
        return listNotes(notes_list=n_list)
    else:
        return 'createERROR'