# Teachers-Portal

**Setup Instructions**

Follow these steps to set up the project on your local machine:

Install PostgreSQL

Download and install PostgreSQL from https://www.postgresql.org/download/.

Create the Database

Open the PostgreSQL shell and run:

CREATE DATABASE "Portal";

Configure Environment Variables

Create a .env file in the project root with the following content (replace username and password with your PostgreSQL credentials):

DATABASE_URL=postgresql://username:password@localhost:5432/Portal
SECRET_KEY=mysecretkey

Install Dependencies

Run the following command to install required Python packages:

pip install -r requirements.txt

Initialize the Database

Run these commands to set up the database migrations:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Start the Application
Run the application with:
python run.py

Your application should now be running locally.
