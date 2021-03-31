# Track profile changes & email on change
from playwright.sync_api import sync_playwright
from email.mime.text import MIMEText

from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib, ssl
import logging
import json
import time
import urllib.parse


# load settings
with open("settings.json", 'r') as settings_raw:
    settings = json.loads(settings_raw.read())

    SMTP_PORT = settings['smtp_port']
    SMTP_SERVER = settings['smtp_address']
    SENDER_EMAIL = settings['sender_email']
    SENDER_EMAIL_PASS = settings['sender_email_password']
    WEBSITE_HOMEPAGE_URL = settings['website_homepage_url']

def send_email(email, profile, notifier):
    subject = f"{profile['name']} has changed their LinkedIn Profile"
    delete_notifier_link = f"{WEBSITE_HOMEPAGE_URL}/delete-notifier/{notifier['uuid']}/{urllib.parse.quote(str(email))}"
    mail_message = f"The user <a href='{profile['url']}'>{profile['name']}</a> has changed their profile picture<br><a href='{delete_notifier_link}'>Unsubscribe From This LinkedIn User</a>"

    msg = MIMEText(mail_message, 'html')
    msg['Subject'] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())

    logging.info(f"Sent email to: {email}")

def extract_profile(url, page):
    page.goto(url)
    # wait for page load
    page.wait_for_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[2]/div[1]/h1')
    time.sleep(10)

    # extract name & avatar url
    name = page.query_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[2]/div[1]/h1').inner_text()
    avatar_url = page.query_selector('xpath=//*[@id="main-content"]/section[1]/section/section[1]/div/div[1]/img').get_attribute('src')

    return {'name': name, 'avatar_url': avatar_url, 'url': url}

def check_for_updates():
    with open("data.json", 'r') as inp:
        notifiers = json.loads(inp.read())['profiles_to_track']
        with sync_playwright() as p:
            # launch playwright
            browser = p.chromium.launch(headless=False)
            # with proxy
            #browser = p.chromium.launch(headless=False, proxy = {'server': "http://40.85.152.26:8080", 'port': '8080'})

            # create new page
            page = browser.new_page()

            # visit all the profiles
            for profile in notifiers:
                try:
                    cur_profile = extract_profile(profile['url'], page)
                except:
                    continue
                current_profile_image = cur_profile['avatar_url']

                if profile['previous_image'] == "":
                    # triggered when a recently added notifier is added to the database
                    # but we haven't fetched a new image for the linkedin user yet
                    profile['previous_image'] = current_profile_image
                elif current_profile_image != profile['previous_image']:
                    for email in profile['emails']:
                        send_email(email, cur_profile, profile)
                    # set previous image to the current image used on the profile
                    profile['previous_image'] = current_profile_image

            # close playwright
            browser.close()

    # write the new JSON to the data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({'profiles_to_track': notifiers}, f, ensure_ascii=False)

check_for_updates()

'''
sched = BlockingScheduler()
sched.add_job(check_for_updates, 'cron', hour='0')

sched.start()
'''
