# Mamma Mia Pizzeria - Staff Dashboard

🎥 WATCH OUR VIDEO PRESENTATION HERE:
[https://www.youtube.com/watch?v=0GjsitGQNsw](https://www.youtube.com/watch?v=0GjsitGQNsw)
My phone ran out of storage, so I could only upload it this way, enjoy! 😊

This is an application for Mamma Mia Pizzeria


## Project Structure

- `pizza_project/Modelling/` – Database schema for the project.
- `pizza_project/ddl_script.sql` – Run this to create the database tables.
- `pizza_project/insert_data.sql` – Insert sample data into the tables.
- `pizza_project/queries.sql` – Database queries.

- `pizza_project/Application/src/Application.py` – Main Flask application.
- `pizza_project/Application/src/methodsORM.py` – SQLAlchemy ORM methods for querying the database.
- `pizza_project/Application/src/templates/` – HTML templates for the dashboard.


## Setup Instructions

1. Install dependencies:

pip install flask sqlalchemy pymysql

2. Update your MySQL password in Application.py at line 8:

engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost/pizza_ordering", echo=True)

Replace YOUR_PASSWORD with your actual MySQL password.

3. Run the application:

python Application.py

