## Setup

1. `git clone https://github.com/srujanrouthu/colabel-code.git`
2. `cd colabel-code`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py add_new_images --file_path flowers.csv`
6. Create new webhook on the classifier app on slack at https://api.slack.com/apps/AQVQEQ3K7/incoming-webhooks?
7. Add this webhook URL to `settings.py` on line 126
8. `ngrok http 8000`
9. Add ngrok URL to slack interactive components at https://api.slack.com/apps/AQVQEQ3K7/interactive-messages?
10. `python manage.py runserver`
11. (Optional) Go to 127.0.0.1:8000/start to start the classifier app
12. Go to slack channel #srujan and start classifying images