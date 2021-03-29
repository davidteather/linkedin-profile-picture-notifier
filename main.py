from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
from typing import Optional
import json
import uuid

'''
Project Specifications
----------------------
1. A form with an email to notify & a LinkedIn url to track
2. A json file acting as a database to store these email & LinkedIn pairs
3. A function that runs once a day to compare & update the current profile picture of a LinkedIn user if different send email
4. Function to email when a new profile image is detected
'''

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def return_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/add-notifier')
def add_notifier(request: Request, email: str = Form(...), linkedInUrl: str = Form(...)):
    with open("data.json", 'r') as data:
        data_json = json.loads(data.read())

    data_json['profiles_to_track'].append({
        "uuid": str(uuid.uuid4()),
        "emails": [email.split(",")],
        "url": linkedInUrl,
        "previous_image": "",
    })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False)
    return templates.TemplateResponse("index.html", {"request": request, "success": True})


@app.get("/delete-notifier/{uuid}", response_class=HTMLResponse)
def read_item(request: Request, uuid: str):
    with open("data.json", 'r') as data:
        data_json = json.loads(data.read())

    for item in data_json['profiles_to_track']:
        if item['uuid'] == uuid:
            data_json['profiles_to_track'].remove(item)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False)
    return templates.TemplateResponse("delete_notifier.html", {"request": request})