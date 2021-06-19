# secfi-assignment

## Description
The idea is to create a microservice that allows CRUD operations on a “users” table. The assignment doesn’t have a
hard time limit but we also don’t want to take too much of your time, so try to spend a maximum of 4/5 hours on it.
The service should allow read and write operations following this interface:
```json
interface IUser {
    firstName: string;
    lastName: string;
    userName: string;
    password: string;
    avatar: string;
}
```
- Service should be written in Python or TypeScript
- Service should run in a Docker container
- Password should be stored in encrypted format
- For the avatar, pick a way of storing you think is most efficient
- Database can be any type (Postgresql, MySQL, SQLite)

## Solution
I created the microservice using Python 3.7+ and the Django framework. The microservice exposes a GraphQL API implemented using the [graphene-django](https://docs.graphene-python.org/projects/django/en/latest/) app and enables the client to perform CRUD operations on a custom `User` table stored in SQLite.

## How much time did you end up spending on it?
Around 10 hours. I exceeded with the hours because I had to learn how to implement GraphQL using Graphene in Django.

## What are some of the design decisions you made?
1. I used Python & Django since it is the language and framework I am most familiar with
2. I used a SQLite in order to complete the assignment as fast as possible. I did not want to deal with the intricacies of setting up and connecting to a database
3. Security features have been disabled for this microservice because I assumed that the User microservice is an internal service that is called by other microservices (such as the "Authentication" microservice) in the system. In other words, cookied or JWT based authentication and authorization have not been enabled. CSRF protection is also disabled. Also, the API does not support rate limiting
4. I did not spend time thinking about limiting the request payload size. It's the Django default `DATA_UPLOAD_MAX_MEMORY_SIZE` (2.5MB)
5. Because the User microservice should do one thing and one thing well I offloaded the handling of the "avatar" image to another external service called [ImgBB](https://api.imgbb.com/). I also assumed that "most efficient" mentioned in the description refers to development time and not the performance of the application.
6. I assumed that the value of the "avatar" property sent in the request is a base64-encoded image. The response of the "avatar" property is a link to the image stored in [ImgBB](https://api.imgbb.com/
7. Each username is unique in the `User` table
8. I used the default PBKDF2 hasher included in Django to hash the user plaintext password

## What do you like about your implementation?
I believe the implementation is easy to read and comprehend for a person familiar with Django and Graphene.

## What would you improve next time?
This is a very basic implementation of the User microservice and there is a lot of room for improvement with it. Given more time I would:
1. Clarify the requirements regarding the expected input and output of the API. I did not clarify the requirements here because I had to complete the exercise in the weekend since I wouldn't find the time to do so in the coming week
2. Add filtering and pagination to the `allUsers` query, i.e. the query that returns all of the users in table
3. Add support for partial updates, i.e. the ability to update a subset of attributes of the user in a mutation
4. Improve API error messaging
5. Include retries to the ImgBB api in case an internal server error or rate limit error occurs. Or maybe even scrap the dependency of this API because it severely limits the performance of the User microservice
5. Perform stronger validation against passwords. For example, check if the password is entirely numeric or is in a list of common passwords
6. Add random salt to password hashing
7. Use an external PostgreSQL or MySQL database and not SQLite
8. [Add unit tests](https://docs.graphene-python.org/projects/django/en/latest/testing/)
9. Dockerize the Django application with a production ready WSGI server such as [gunicorn](https://gunicorn.org/)
10. Improve logging. For example, the logs do not provide information about which `Query` or `Mutation` handler is called or more details about errors
11. Deploy the dockerized application to a demo server in order to make it easier for the reader to try out the API
12. [Switch implementation](https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/) to support [Relay](https://relay.dev/) since a lot of extra functionality (such as filtering and pagination) is included in the graphene relay implementation

Given even more time and information about how the user microservice will be internally integrated with the rest of the microservices in the system I would also:
1. Set up health check endpoint that will be used for load balancers
2. Set up the infrastructure for the user microservice
3. Maybe include authentication / authorization that will check the validity of JWT tokens generated by the "authentication" microservice
4. Set up rate limiting. Rate limiting in this case could be done using a custom HTTP header that corresponds to each microservice that uses the user microservice
5. Ship logs to a monitoring service such as Splunk and set up alerts

## How to run demo server with Docker
1. Run `docker-compose up --build` This will spin up a Django development server in http://localhost:8000
2. Make GraphQL requests to `http://localhost:8000`. See request examples in the [Postman collection](postman)

 ## How to setup the development environment
1. Install [poetry](https://python-poetry.org/)
2. Run `poetry install`
3. Run `poetry run manage.py runserver`
4. Go to `http://localhost:8000` since GraphiQL explorer is enabled
