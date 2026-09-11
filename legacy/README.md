# PINGME

![PingMe](readme_assets/responsive.png)

This section of the project provides a Django Rest Framework API for the [PingMe!](https://ping-me-pp5-frontend-c34a5313765d.herokuapp.com) react web app. It has also been designed and optimzed for mobile environments in the future.

---

Ping me is a lightweight discord clone that allows the user to view signup and join chatrooms to chat with other users, the sole aim of the project is to document my skills with react/typescript mui and django rest framework

As this is a backend site there is no deployed site to visit but you can view the schema [here](https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/docs/schema/ui/#/) this has a list of endpoints and what they do, sadly they are not interactable as for security the endpoints are all protected by authentication requirementss

## Table of contents
- [PingMe](#pingme)
  * [Project goals](#project-goals)
  * [Table of contents](#table-of-contents)
  * [Planning](#planning)
  * [Data models](#data-models)
  * [API endpoints](#api-endpoints)
  * [Frameworks, libraries and dependencies](#frameworks-libraries-and-dependencies)
  * [Testing](#testing)
  * [Bugs](#bugs)
  * [Deployment](#deployment)
  * [Credits](#credits)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Planning
Planning started by creating epics and user stories for the frontend application, based on the project goals. The user stories were used to inform wireframes mapping out the intended functionality and 'flow' through the app. From there we build the various models and endpoints out to meet these goals

### Data models
Data model schema were planned in parallel with the API endpoints, using an entity relationship diagram.

[ERD Diagram](readme_assets/erd.png)

For this project seeing as an ERD diagram was essential for app planning, i built one to cover what we needed out of this application, as the user is the one who will be in control of everything from server and channel creation to the chatting we decided to put them as the primary focal point, various features like the server and conversation models are tied back to the user via foreign keys. And uses viewsets to execute the various functions and abilities of the api. Below i will cover the custom models a bit

#### **Account**
Represents the user Account, using a one-to-one relationsip to the user model. A Account instance is automatically created on user registration. The Account model includes includes various fields that we the dev can use to distinguish it and link it to other parts of the app

#### **Server**
This model handles all of our server logic, including creation editing and deleting, its' used in the front end by our server context consumers to pass server data efficiently and easily

#### **Category**
The category is our primary sorting model for servers, upon server creation it is given a category to be filtered by we then utilized these so users can view the servers that appealed to them

### **Channel**
The channel model was responsible for our channel creation and management, and allows us to enter the channel and chat to users via the messenger / conversation model

### **Conversation**
The conversation model handles storing all of our conversation message objects, this allowed us to have hundreds of messages per conversation and load them all rapidly from our api to our frontend

### **Message**
This was our chief message model each one created a message object, we took this approach to ensure that messages were easy to manipulate

## API endpoints

A list of all api endpoints can be found in our [schema](https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/docs/schema/ui/#/) 
To test this schema and the api endpoints the tester must be authorized, to authorize use the test user credentials provided or create an account, and 
run the token auth endpoint to get an auth token. Posting said auth token into the authorize will allow you access to the scema api

## Frameworks, libraries and dependencies
### django-cloudinary-storage
https://pypi.org/project/django-cloudinary-storage/

Enables cloudinary integration for storing user Account images in cloudinary.

### dj-allauth
https://django-allauth.readthedocs.io/en/latest/

Used for user authentication. While not currently utilised, this package enables registration and authentication using a range of social media accounts. This may be implemented in a future update.

### dj-rest-auth
https://dj-rest-auth.readthedocs.io/en/latest/introduction.html

Provides REST API endpoints for login and logout. The user registration endpoints provided by dj-rest-auth are not utilised by the Serverhub frontend, as custom functionality was required and implemented by the Serverhub API.

### djangorestframework-simplejwt
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Provides JSON web token authentication.

### dj-database-url
https://pypi.org/project/dj-database-url/

Creates an environment variable to configure the connection to the database.

### psychopg2
https://pypi.org/project/psycopg2/

Database adapater to enable interaction between Python and the PostgreSQL database.

### django-cors-headers
https://pypi.org/project/django-cors-headers/

This Django app adds Cross-Origin-Resource Sharing (CORS) headers to responses, to enable the API to respond to requests from origins other than its own host.
ServerHub is configured to allow requests from all origins, to facilitate future development of a native movile app using this API.

### django-channels
https://channels.readthedocs.io/en/latest/

This django add on was our primary means of setting up and maintaining websockets for real time communication coupling this with redis servers from heroku allowed us to create a fully functioning real time application akin to discord

## Testing

Full testing can be found in the testing.md file found [here](https://github.com/ShaAnder/Ping_Me_Backend/blob/main/TESTING.md)

## Future Features

While this api is largely complete I feel there are a few ways I could have improved upon it, such as adding the ability to message batch and changing how the conversation model works when getting user messages. SO these are key features I plan to take a look at after I complete the course.

## Deployment
The api is deployed to heroku via github utilizing a redis key value pair package (Heroku key value pair)

TO deploy this app, you must do the following:

- Clone or fork both repos
- Link them to heroku projects
- The frontend repo requires no more setup

for the backend repo you need to get the heroku key value pair package and setup a cloudinary account, you also need a postgres server

- Next set the following environment variables

ALLOWED_HOSTS - Backend heroku app
CLIENT_ORIGIN - Frontend heroku app
CLIENT_ORIGIN_DEV - For testing locally (use ngrok to tunnel)
CLOUDINARY_API_KEY - For image uploading
CLOUDINARY_API_SECRET
CLOUDINARY_CLOUD_NAME
DATABASE_URL - Postgres DB
DISABLE_COLLECTSTATIC - For staticfiles
HOST_EMAIL - For email functionality
HOST_PW
REDIS_URL - For websockets
SECRET_KEY - for signed data transfer

The redis url comes from heroku Key Value pair and is automaitcally set when you add the package

once these are set the app should run out of the box, you will need to create an admin account for admin actions but beyond that a created user account can do all the functions described in the app on the frontend. All endpoints are protected and require credentials from the get go however this can be disabled by removing the isauthenticated permissions from the various serializers and viewsets

## Credits
Credit goes to the various documentation that helped me figure this out:

- [Django documentation](https://www.djangoproject.com)
- [Django Rest Framework documentation](https://www.django-rest-framework.org)
- [django-filter documentation](https://django-filter.readthedocs.io/en/stable/)
- [django-recurrence documentation](https://django-recurrence.readthedocs.io/en/latest/)
- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [dateutil documentation](https://dateutil.readthedocs.io/en/stable/index.html)

As well as very academy for teaching me the basics of websocket setup and communication
