# Chatbot

### Prerequisites
1. Git
2. Python (version 3 or above)

### Setup

```sh
$ git clone https://github.com/Vaishnavi23022003/Cinematic.git
$ cd Cinematic
```

Create a virtual environment to install dependencies in:

```sh
$ python -mvenv env
```
if above command does not work due to difference in python versions try:
```sh
$ pip install virtaulenv
$ virtualenv env
```

Activate the virtual environment
```sh
$ env/scripts/activate
```
if above command does not work due to difference in python versions try:
```sh
$ source env/bin/activate
```
if it still doesn't work then find the activate file in env folder and use it's path


Then install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```
if above command does not work due to difference in python versions try:</br>
use `py -m pip install` in place of  `pip install`

Note the `(env)` in front of the prompt. </br>
This indicates that this terminal session operates in a virtual environment set up.</br>

Once `pip` has finished downloading the dependencies:
```sh
(env)$ pip install django
(env)$ django-admin startproject temp
```

A temp folder will be created -> we only need this for django `SECRET_KEY`.<br />
Go to `temp/temp/settings.py` and copy the value of `SECRET_KEY`.<br />
Now got to `../../Cinematic/settings.py` and replace the value of `SECRET_KEY` with the copied one.<br />
Also change `<db_user_name>` with the name of postgresql database and `<db_password>` with password of postgresql database.</br>

Now:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`
