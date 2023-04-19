# Helpdesk API build with Django REST Framework

## Main idea:
Creating tickets to solve problems

## Key concepts:

## To run application on local machine:
**1. Clone the repository:**

``` git clone https://github.com/rytpQWE/Helpdesk.git ```

**2. Build docker compose:**

``` sudo docker compose build ```

**3. Start docker compose:**

``` sudo docker compose up ```

**4. Apply the migrations:** <br>
Go to another terminal where the project is located <br>
``` sudo docker compose exec web python manage.py migrate ```

**5. From now local version is available at**
http://127.0.0.1:8000/

