# linkedin-profile-picture-notifier

This is a commissioned project that notifies users over email when a person's LinkedIn
profile picture changes. If a person changes their profile image on LinkedIn it may imply
that the individual is looking at jobs at other places as they are actively on LinkedIn.
Recruiters are able to utilize this software in order to be the first to reach out to
individuals tracked by the program.

## Configuration

You will need to configure settings.json here's a template

```
{
    "smtp_address": "",
    "smtp_port": 0,
    "sender_email": "",
    "sender_email_password": "",
    "website_homepage_url": "",
    "linked_in_username": "",
    "linked_in_password": ""
}
```

**What do these keys mean?**

- smtp_address: This is the address of your email smtp server
- smtp_port: This is the port of your email smtp server
- sender_email: This is the email you want to send the notifications from
- sender_email_password: The password to the email above
- website_homepage_url: The URL to access the main page that FastAPI provides, do **not** include the slash at the end see the sample below
- linked_in_username: The username/email of the LinkedIn user to log into. You must not have two factor authentication enabled.
- linked_in_password: The password of the LinkedIn user to log into. You must not have two factor authentication enabled.

Here's a sample settings.json that uses a gmail account to send the emails. To do this you'll have to [enable less secure apps](https://support.google.com/accounts/answer/6010255?hl=en) on your gmail account you want to send the emails from.

```
{
    "smtp_address": "smtp.gmail.com",
    "smtp_port": 465,
    "sender_email": "youremail@gmail.com",
    "sender_email_password": "yourpassword",
    "website_homepage_url": "http://127.0.0.1:8000",
    "linked_in_username": "",
    "linked_in_password": ""
}
```

## Setup and installation

Software Requirements
```
Python 3.8+
```

Install dependencies
```
pip install -r requirements.txt
python -m playwright install
```

Run FastAPI server (handles website)

```
uvicorn main:app --reload
```

Run background.py (checks if LinkedIn profile changed)

```
python background.py
```

## Authors

* **David Teather** - *Initial work* - [davidteather](https://github.com/davidteather)
* **Nick Filerman** - *Initial work* - [nickfilerman](https://github.com/nickfilerman)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
