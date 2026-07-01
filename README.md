# Contalink test backend

## How to run locally

Clone the repo:
```
git clone git@github.com:omezaldama/contalink-test-be.git
```
Cd into the repo directory and create a virtual environment:
```
cd contalink-test-be
virtualenv .venv
```
Activate the virtual environment:
```
. .venv/bin/activate (Linux)
source .venv/bin/activate (Mac)
```

Once inside the virtual environment, install dependencies:
```
pip install -r requirements.txt
```

Copy the environment variables file:
```
cp .env.example .env
```

You will need Redis for the caching functionality. The easier way to set it up is using docker. On a different terminal, run:
```
docker run -p 6379:6379 --rm redis
```

Now open the `.env` file and write the appropiate values for the following variables:
- `DB_HOST`: the host of the postgres database
- `DB_DATABASE`: the name of the database to be used
- `DB_USERNAME`: the username of the postgres database
- `DB_PASSWORD`: the password for the databse user
- `RESEND_API_KEY`: this service uses [Resend](https://resend.com/) to send the notification emails. You will need to get an API key and write it here.
- `EMAIL_RECEIVER`: the email to which the notification emails will be sent.

If you are not using the docker setup for Redis you will also need to set `REDIS_HOST` and `REDIS_PORT` with the appropriate values.
You can use the `REDIS_TTL_MINS` variable to control the cached results TTL (in minutes).

Finally, inside the virtual environment, run
```
uvicorn app.main:app
```
The app will run on port 8000 by default.
