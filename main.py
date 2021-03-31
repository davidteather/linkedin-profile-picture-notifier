from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
from typing import Optional
import logging
import json
import uuid
import os

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
        try:
            data_json = json.loads(data.read())
        except json.decoder.JSONDecodeError:
            # handles if file doesn't exist or data is invalid
            if os.path.isfile('data.json'):
                with open("data.json", 'w+') as out:
                    out.write('{"profiles_to_track": []}')
                    data_json = {"profiles_to_track": []}
            else:
                logging.critical("data.json is formatted incorrectly")

    temp_item = None
    for item in data_json['profiles_to_track']:
        if item['url'] == linkedInUrl:
            temp_item = item

    if temp_item:
        temp_item['emails'].extend(email.split(","))
        temp_item['emails'] = list(set(temp_item['emails']))

    else:
        data_json['profiles_to_track'].append({
            "uuid": str(uuid.uuid4()),
            "emails": list(set(email.split(","))),
            "url": linkedInUrl,
            "previous_image": "",
        })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False)
    return templates.TemplateResponse("index.html", {"request": request, "success": True})


@app.get("/delete-notifier/{uuid}/{email}", response_class=HTMLResponse)
def read_item(request: Request, uuid: str, email: str):
    with open("data.json", 'r') as data:
        data_json = json.loads(data.read())

    for item in data_json['profiles_to_track']:
        if item['uuid'] == uuid:
            for mails in item['emails']:
                if mails == email:
                    item['emails'].remove(mails)

                    if len(item['emails']) == 0:
                        data_json['profiles_to_track'].remove(item)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False)

    return templates.TemplateResponse("delete_notifier.html", {"request": request})
