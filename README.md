# Django Blog API Server 
This project is a blog CRUD REST API server.

<img src="https://img.shields.io/badge/python-3.8-blue"/> <img src="https://img.shields.io/badge/coverage-99%25-brightgreen"/>
<img src="https://img.shields.io/badge/Django-3.0-164834"/>
<img src="https://img.shields.io/badge/Zappa-0.54-black"/>

### Prerequisites / 선행 조건

```
Python3.8
```

## Usage (local)

```
$ git clone https://github.com/na86421/django-blog-api.git
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip install -r requiremnets.txt
$ python manage.py migrate
$ python manage.py runserver
```

## Running the tests

```
$ coverage run manage.py test
$ coverage report
$ coverage html
```

## Usage API server
It is deployed in aws lambda and you can use the API url below.   
https://8u96f9df9h.execute-api.ap-northeast-2.amazonaws.com/dev/swagger/


## Built With

* [JunKi Yoon](https://github.com/na86421)


