# Mamma Mia Pizzeria - Staff Dashboard

This is an application for Mamma Mia Pizzeria


## Project Structure

- `pizza_project/Modelling/` – Database schema for the project.
- `ddl_script.sql` – Run this to create the database tables.
- `insert_data.sql` – Insert sample data into the tables.
- `queries.sql` – Normal database queries for testing.

- `Application/src/Application.py` – Main Flask application.
- `Application/src/methodsORM.py` – SQLAlchemy ORM methods for querying the database.
- `Application/src/templates/` – HTML templates for the dashboard.


## Setup Instructions

1. Install dependencies:

pip install flask sqlalchemy pymysql

2. Update your MySQL password in Application.py at line 8:

engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost/pizza_ordering", echo=True)

Replace YOUR_PASSWORD with your actual MySQL password.

3. Run the application:

python Application.py

