# linkedin-profile-picture-notifier
This is a commissioned project that notifies users over email when a person's LinkedIn profile picture changes


## Setup and installation

With virtualenv
```
virtualenv env
cd env/Scripts
activate
cd ../../
pip install -r requirements.txt
python -m playwright install
```

Without virtualenv
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
TODO
```