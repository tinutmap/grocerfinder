# grocerfinder.com

## Intro
grocerfinder.com is a pet project to keep a curated list of seasonal items from **Aldi** grocery store in the US. **Aldi** is author's favorite grocery store which offers rotating high quality seasonal items. Based on author experience, some items are in high demand that are truely *"here today, gone tomorrow"*.

This project's objectives are to:
- Let users keep track of their favorite items.
- Let users rate and discuss about items.
- Provide them a time estimate/prediction of future availability.

The data is gathered from the author and potentially crowd-sourced from public in the future.

 ___
## Tech stack:
This project is also a learning/tinkering/proven ground for the following:
- Database: Postgres.
- Backend: Python, Django, graphene, graphene-jwt.
- Web API: Graphql.
- Frontend: Vuejs, Apollo API Client.
- Deployment: Docker, Nginx, Letsencrypt + Certbot, Linux Ubuntu on Amazon EC2.
___
## For developers
### Prerequisites:
- Postgres 12.0 or higher. [Instruction](https://www.postgresqltutorial.com/postgresql-getting-started/).
- Python 3.8.5 or higher. [Instruction](https://wiki.python.org/moin/BeginnersGuide/Download)
- Pipenv. [Instruction](https://pypi.org/project/pipenv/). Other Python virtual environment management packages can be used, follow their instructions for details.
- Nodejs version 12.18.3 or higher for npm. [Instruction](https://nodejs.org/en/download/package-manager/).
- Git version control 2.24.1 or higher. [Instruction](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Visual Studio Code -- VSCode (recommended) Text Editor/IDE. [Instruction](https://code.visualstudio.com/docs/introvideos/basics).


### Setup:
**Note: the instructions below run under in Windows 10, Git Bash terminal**.
- Clone the repo:
```
git clone https://github.com/tinutmap/grocerfinder.git
```
- Django setup (backend):
  - In terminal, change directory to project root (etc), create new virtual environment and install the required packages by:
  ```
  $ cd grocerfinder
  $ pipenv shell
  $ pipenv install requests
  ```

  - From project root directory, change to Django root directory:
  ```
  $ cd grocerfinder_root
  ```
  - Create `.env` environment variable file in `/grocerfinder/grocerfinder_root/grocerfinder/settings/development`. Create new `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`:
  ```
  # Instruction to generate new secret_key https://tech.serhatteker.com/post/2020-01/django-create-secret-key/ 
  DJANGO_SECRET_KEY=[django_secret_key]

  DJANGO_DEBUG=True

  # env below used in settings.py and database_postgres container
  POSTGRES_DB=grocerfinder
  POSTGRES_USER=grocerfinder_root
  POSTGRES_PASSWORD=[a_secured_password]
  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
   ```
  - Migrate to the database:
  ```
  $ cd grocerfinder_root
  python manage.py migrate
  ```
  - Create a superuser. Type command below and put info into the prompts:
  ```
  $ python manage.py createsuperuser
  ```
  - Start Django backend server by:
  ```
  $ python manage.py runserver 0.0.0.0:8000 
  ```
- Vue setup (frontend)
  - From current directory (`/grocerfinder/grocerfinder_root/`), change to Vue root directory:
  ```
  $ cd ./vueapps/grocerfinder/
  ```
  - Install packages by npm:
   ```
   $ npm install
   ```
   - Run backend server by:
   ```
   $ npm run serve
   ```
   - Browse the website at `https://localhost:8080`

## Deployment (for reference only):
### Prerequisites:
- A server already setup with public IP
- grocerfinder.com domain up with DNS record pointed to server's public IP
- Docker 19.03.13 or higher with docker engine and docker-compose installed on host(dev) machine and remote. [Instruction](https://www.postgresqltutorial.com/postgresql-getting-started/)

### Setup
At project root directory (`/grocerfinder`), create a remote context to server's docker deamon
```
$ docker context create remote \
  --docker "host=ssh://ubuntu@grocerfinder.com"
```
- Create `.env` environment variable file in `/grocerfinder/grocerfinder_root/grocerfinder/settings/production`.
```
DJANGO_SECRET_KEY=[django_secret_key]
DJANGO_DEBUG=False

# env below used in settings.py and database_postgres container
POSTGRES_DB=grocerfinder
POSTGRES_USER=grocerfinder_root
POSTGRES_PASSWORD=[a_secured_password]
POSTGRES_HOST=database # database is the container defined in docker-compose.yml
POSTGRES_PORT=5432

# container init env variables

# Set super user password in Docker container if desired, leave blank if no super user created
DJANGO_SUPERUSER_PASSWORD=[another_secured_password]
```

Optional: In `grocerfinder/Dockerfile` Change the following options if needed. Default values are shown
```
# Set to True if wanting to Flush data upon container init. 
# Warning will delete current data
ENV DJANGO_FLUSH_DATA=False

# Set to True if wanting to Flush data upon container init. 
ENV DJANGO_MIGRATE=False

# Set to True if loading data from data.json file
ENV DJANGO_LOAD_DATA=False
```

 To apply new changes to server run script
```
$ sh deploy.sh
```




