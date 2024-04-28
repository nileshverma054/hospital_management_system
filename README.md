# Hospital Management System 🏥
A RESTful API for a Hospital Management System using Python Flask framework that allows users to manage patients, doctors, and departments efficiently.


### Tech Stack
- Python 3.12.1
- Flask 3.0.3
- Flask-Restful
- SQLAlchemy
- MySQL


## API Document
Use the below link to view API documentation
[Postman API Documentation](https://documenter.getpostman.com/view/15731252/2sA3Bt1UqN) 🔥

## Project Setup
###### Steps
- Clone Repostory
- cd to project folder

### Running the application with Docker Compose 🐳
To run the application locally, you will need to have Docker and Docker Compose installed on your machine.
Once you have Docker and Docker Compose installed, you can use the following commands to start the application:

```
docker-compose build
```
```
docker-compose up
```

##### Or - unfortunaltely if you do not have docker then you can setup manually using below steps
###### Requirements
- Mysql
- Python 3.12

###### Steps
- Create virtual environment
```
python3.12 -m venv .venv
```
- Activate virtual environment
```
source .venv/bin/activate
```
- When running for first time, use below command to perform necessary databse migrations
```
bash db_setup.sh
```
- Run the project using development server
```
bash startup.sh
```


### TODO

- [x] Project initialization
  - [x] Create a new Python virtual environment
  - [x] Initialize a new Flask app
  - [x] Set up database (SQLAlchemy)
  - [x] Configure Flask-RESTful
  - [x] Set up logger

- [x] Models
  - [x] Patient
  - [x] Doctor
  - [x] Department

- [x] Containerise App
  - [x] Set up Dockerfile
  - [x] Set up Docker-Compose


- [ ] Routes
  - [x] Department
  - [ ] Patient
  - [ ] Doctor

- [ ] Resources
  - [x] Department
  - [ ] Patient
  - [ ] Doctor

- [x] Documentation
  - [x] Postman

- [ ] Tests
  - [x] Unit tests
  - [ ] Integration tests

- [ ] Create internal python library
  - [ ] utils library
    
