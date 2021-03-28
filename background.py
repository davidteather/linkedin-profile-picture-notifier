# Track profile changes & email on change
from playwright.sync_api import sync_playwright

import apscheduler
import smtplib, ssl
import logging
import json
import time

with open("settings.json", 'r') as settings_raw:
    settings = json.loads(settings_raw.read())

    SMTP_PORT = settings['smtp_port']
    SMTP_SERVER = settings['smtp_address']
    SENDER_EMAIL = settings['sender_email']
    SENDER_EMAIL_PASS = settings['sender_email_password']

def send_email(email, profile):
    mail_message = f"The user {profile['name']} has changed their profile picture\n Url: {profile['url']}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, email, mail_message)

    logging.info(f"Sent email to: {email}")

def extract_profile(url, page):
    page.goto(url)

    # wait for page load
    page.wait_for_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[2]/div[1]/h1')

    # extract name & avatar url
    name = page.query_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[2]/div[1]/h1').inner_text()
    avatar_url = page.query_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[1]/img').get_attribute('src')

    return {'name': name, 'avatar_url': avatar_url, 'url': url}

# apschedule this to run at some time
def check_for_updates():
    with open("data.json", 'r') as inp:
        notifiers = json.loads(inp.read())['profiles_to_track']
        with sync_playwright() as p:
            # launch playwright
            browser = p.chromium.launch(headless=False)

            # create new page
            page = browser.new_page()

            # visit all the profiles
            for profile in notifiers:
                cur_profile = extract_profile(profile['url'], page)
                current_profile_image = cur_profile['avatar_url']
                if current_profile_image != profile['previous_image']:
                    for email in profile['emails']:
                        send_email(email, cur_profile)
                    # set previous image to the current image used on the profile
                    profile['previous_image'] = current_profile_image

            # close playwright
            browser.close()

    # write the new JSON to the data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(notifiers, f, ensure_ascii=False, indent=4)