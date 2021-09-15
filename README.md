# pdviz
Proposal Development Visualization

#### Deployment
* Install dependencies from requirements.txt file
* Clone the dependent repos, [feedback](https://github.com/mercycorps/feedback) and [djangocosign](https://github.com/mercycorps/djangocosign)
* Make sure the local.py file is up-to-date.
* 










# pdviz

Proposal Development Visualization

## SETUP INSTRUCTIONS

### TESTED ENVIRONMENT
- Python 3.6.x - 3.8.x
- djangorestframework-3.12.4
- Django 3.2.7


### DEPENDENCIES
1. Install python3-dev
2. Install mysql


## INSTALL DJANGO CODEBASE
### Clone the repo and create a virtualenv for python3
Create a directory for this project which will contain the repo and the virtualenv.
```bash
$ mkdir /Users/<username>/pdviz_dir
$ cd pdviz_dir
$ git clone https://github.com/mercycorps/pdviz.git
$ virtualenv -p python3.8 venv
$ source venv/bin/activate  # you should see '(venv)' appear on the left of your command prompt
```

### Activate the virtualenv and `pip-sync requirements.txt`
Install `pip-tools` and use the `pip-sync` command to install, upgrade, and uninstall your virtual environment with the necessary dependencies to match the `requirements.txt` contents.
```bash
$ pip install pip-tools
$ pip-sync requirements.txt
```

### Copy local_example.py to local.py and modify as needed.
Modify at minimum the following fields:
    ```yaml
    SECRET_KEY: "your_key_here"
    SETTINGS_DIR: "XXXXXXXXXXX"
    DATABASES:
        default:
            NAME: "<db_name>" # "pdviz"
            ENGINE: "django.db.backends.mysql"
            HOST: "localhost"
            USER: "<db_usernaem>" # "root"
            PASSWORD: "<password>" # "SooperSekritWord"
            PORT: ""
        gait:
            NAME: "<db_name>" # "grants"
            ENGINE: "django.db.backends.mysql"
            HOST: "localhost"
            USER: "<db_usernaem>" # "root"
            PASSWORD: "<password>" # "SooperSekritWord"
            OPTIONS:
                charset: "latin1"
    ```

### Copy the saml_config_example.yml file to saml_config.yml.  
To enable the Okta login on a server, the values for each of the settings in the saml_config.yml will need to be updated with your own values and/or those from an Okta XML config file sent to you by the Okta administrator. 

## Creating a local user
You will need to create a local user so you can log in.
You can use MySQL to create a local superuser

#### Using MySQL
Use the `createsuperuser` command and enter in a username and password to be used to login. When it asks for an email, you can just hit the Enter key to skip the question (email not needed to login).
```bash
$ python manage.py createsuperuser
Username: <my_username>
Email address:
Password: <my_password>
Password (again): <my_password>
Superuser created successfully.
```