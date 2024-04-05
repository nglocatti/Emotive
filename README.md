# Take Home - Django Skeleton

## Getting Started
Dependencies:
* Docker - See [Get Docker](https://docs.docker.com/get-docker/)
* Docker Compose - Installed with Docker Desktop, See [Install Docker Compose](https://docs.docker.com/compose/install/)

With the dependencies installed, running the project is as simple as running:
```bash
docker compose up
```

This will pull the required Docker images and spin up a container running your service on http://localhost:8000.

To end the service, press `Ctrl+C`

## The Activity
Build a simple API in Python, using Django or Flask. This API should integrate with a third party service or a database and accomplish something interesting, but also shouldn’t take terribly long to implement - endpoints for one or two resources would be sufficient. This activity shouldn’t take more than an hour or so. If this doesn’t seem like much time - you’re right! We expect that you’ll have to focus on one of a few areas for your API:
* The API design and interface (REST vs. GraphQL)
* Integration with a third-party API OR Integration with a database

### Requirements
1. A clear problem statement - what do you intend the API to accomplish?
2. Dependencies for running the API
3. A code repository link from which your interview can checkout the code OR a .zip file containing the source code
4. A README file in the code root containing instructions for running the API

### Some Ideas...
#### Interesting APIs
* [NASA Open APIs](https://api.nasa.gov/index.html)
* [OpenWeather API](https://openweathermap.org/api)
* [Polygon.io Stocks API](https://polygon.io/)

Plus anything more you can discover
#### Databases
* [SQLite](https://www.sqlite.org/index.html)
* [PostgreSQL](https://www.postgresql.org/)
* [MySQL](https://www.mysql.com/)
* [MariaDB](https://mariadb.org/)

PostgreSQL is provided in our skeleton projects, but another database is fine if you’d prefer.
#### Projects
* A stock recommendation service
* A green/red alert for outdoor activity safety
* A Mars Rover camera viewer


## Solution Overview

This Django application provides functionalities to search for assets using two different APIs: Polygon's reference tickers API and Polygon's stocks/equities aggregates API.

### How to Use
#### Installation:

* Clone the repository to your local machine.
* Install the required dependencies with previous explanation.
* Run migrations to create the necessary database schema using python manage.py makemigrations followed by python manage.py migrate.


#### API Key Setup:

* Use the existing or obtain an API key from Polygon.
* Replace the placeholder API key in the code with your actual API key.

### Run the Application:

* Start the Django development server.
* Access the application in your web browser at http://localhost:8000.

## Usage:

* Navigate to the home page to view all assets.
* Use the asset search form to search for specific assets based on various parameters. http://localhost:8000/asset-search
* View detailed asset information and search results. http://localhost:8000/api/assets/search/

#### Additional Notes
* This application is built using Django and utilizes Django's ORM for database operations.
* It integrates with Polygon's APIs for retrieving asset data.
* Error handling is implemented to handle database connection errors and API request errors.
* The application provides both web views and API endpoints for asset search functionality. http://localhost:8000/api/assets/search/?ticker=META


