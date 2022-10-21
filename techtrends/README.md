# TechTreds Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run 

Steps required:

1. Initialize environment `virtualenv .venv` (tested on python 3.8) and install python dependencies `pip install -r requirements.txt`
2. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
3.  Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint.
4. If everything fail on your local environment, avoid dependency problems and extra operating system configuration using the Docker image build from the docker file in the parent directory!