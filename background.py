# Track profile changes & email on change
import apscheduler
import json

def send_email(email, profile):
    mail_message = f"The user {profile['name']} has changed their profile picture\n Url: {profile['url']}"

def extract_profile(url):
    pass

# apschedule this to run at some time
def check_for_updates():
    with open("data.json", 'r') as inp:
        notifiers = json.loads(inp.read())['profiles_to_track']
        for profile in notifiers:
            cur_profile = extract_profile(profile['url'])
            current_profile_image = cur_profile['avatar_url']
            if current_profile_image != profile['previous_image']:
                for email in profile['emails']:
                    send_email(email, cur_profile)
