# BITS Github API Project
 
## Prerequisites
* Python
* Virtualenv
* Postgres

## Getting Started
1. Clone the repository.
2. Create virtual environment. 
```
virtualenv -p python3 envname --no-site-packages
```
3. Go to project folder
4. Install requirements 
```
pip install -r requirements.txt
```
5. Migrate 
```
python manage.py migrate
```
6. Run project 
```
python manage.py runserver
```
