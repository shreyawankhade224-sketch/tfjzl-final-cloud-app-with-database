# Online Course - Django Final Project

Django app with courses, lessons, an exam (Question / Choice / Submission) and a result page.

## Run locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # creates demo data and logins
python manage.py runserver
```

Logins created by `seed`:
- admin / admin123  (superuser, use at /admin/)
- learner / learner123

Pages:
- /admin/                      admin site
- /onlinecourse/               course list
- /onlinecourse/1/             course details + exam
