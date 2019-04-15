
# Requirements
- Python 3.6 or above
- homebrew *(Only for mac)*
- git
- pip
- pyenv
- virtualenv
- awsebcli *(Only if you wish to deploy on the AWS)*

    
1. Homebrew, pyenv and virtualenv installation setup

    ```
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install pyenv
    brew install pyenv-virtualenv
    sudo pip install --upgrade awscli
    ```
    - *Add the following lines into your bash profile:*
        - *eval "$(pyenv init -)"*
        - *eval "$(pyenv virtualenv-init -)"*
        
    
2. How to build pyenv environments

    ```
    pyenv install 3.7.2
    pyenv virtualenv 3.7.2 backend
    ```

## Software instalation proccess
    
- ### How to get the source code

    `https://github.com/RonildoBragaJunior/smsf-django-api`
    
- ### How to run it:

    - Using the exisitng database. *user:ronildo / password:ronildo*
    ```
    pyenv activate backend
    cd backend-api
    pip install -r requirements.txt
    python manage.py runserver
    ```
    
    - Only if you want to start a fresh database
    ```
    pyenv activate backend
    cd backend-api
    pip install -r requirements.txt
    
    python manage.py flush
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc"  -delete
    rm -rf db.sqlite3
    
    python manage.py makemigrations
    python manage.py migrate
    python manage.py load_food
    python manage.py load_company
    python manage.py load_people
    
    python manage.py dumpdata --exclude=contenttypes --exclude=auth > api/fixtures/dumpdata.json
    python manage.py test
    python manage.py createsuperuser
    python manage.py runserver
    ```
    
    
-  ### How to create an AWS environment for deployment

    *- You have to request/create your aws credentials before you proceed with these steps*
    
    *- If you dont have the credentials, please create yours using this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)*
    
    ```
    eb init -p python-3.6 backend-api
    eb init
    eb create backend-api-prod
    ```
    
    - How to deploy into the AWS environment
    ```
    python manage.py collectstatic
    eb deploy
    eb open
    ```
    
___