<h1 align="center">FraudLens</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20with-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-MySQL-orange?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/AI%20Model-TensorFlow%2FScikit--Learn-yellow?style=for-the-badge" />
</p>

---

**FraudLens** is an AI-powered web platform that detects **scam websites, phishing emails, and SMS frauds**. Users can input URLs, emails, or messages and instantly receive a trust score along with a detailed risk analysis. The system is built using Django for the backend, MySQL for persistent data storage, and a vanilla HTML/CSS/JavaScript frontend. AI models are powered by TensorFlow and Scikit-learn.

Demo video link: **[Youtube](https://youtu.be/AIHhBog-fDw)** (Old)

---

## Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python, Django
* **Database**: MySQL
* **Machine Learning**: TensorFlow, Scikit-learn
* **Deployment-ready**: RESTful API integration

---

## Features

* URL scam detection with AI-based trust scoring
* Email scam detection (phishing, fraud analysis)
* SMS scam classification
* User authentication (Sign Up, Sign In)
* Dynamic dashboard for scanning and result visualization
* LocalStorage to store session info (username)

---

### MySQL Setup

Ensure you have a MySQL database `fraudlens_db` created. In `settings.py`, update your DATABASES section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fraudlens_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

> [!NOTE]
> Use `CREATE DATABASE fraudlens_db` to create database in MySQL if not already created

---

## Running

### Clone the repository

```bash
git clone https://github.com/Rishabh4Jakhar/Fraudlens.git
cd fraudlens/fraudlens_backend
```

### Backend Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
> [!NOTE]
> Server will be running at [http://127.0.0.1:8000](http://127.0.0.1:8000)


---

## Requirements

### fraudlens_backend/requirements.txt

```
django>=4.2
djangorestframework
mysqlclient
django-cors-headers
tensorflow
scikit-learn
```

### frontend (no framework used)

No build tool needed. Vanilla JS, HTML and CSS loaded from `templates/` and `static/` directories.

---

## To-Do

* Replace localStorage with secure JWT/session cookies
* Add user profile page and edit password support
* Deploy frontend as React + TypeScript SPA
* Use Celery/Redis for async model inference
* Email verification and password reset support
* Add rate limiting to public APIs

---

## Contributors

- [Advik Gupta](https://github.com/NOVA2OP)
- [Akshat Bhatt](https://github.com/AkshatBhatt4)
- [Rishabh Jakhar](https://github.com/Rishabh4Jakhar)
- [Tanisha Sharma](https://github.com/whytimmyy) 

---

## Made with <3
