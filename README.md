# Helpdesk API build with Django REST Framework

## Main idea:
Creating tickets to solve problems

## Key concepts:
- Any authenticated user can create, delete a ticket;
  * Also: add images, comment, name of ticket, category selection
- Tickets are only visible to their creators;
- Tickets have only two types(Accepted, Completed):
  * When creating a ticket, the status == "accepted" by default and sends a mail to all employees<br>
    Tickets with status "accepted" available on ``` "/api/desk" ```
  * Tickets with status "completed" available on ``` "/api/completed_desk" ```
- There is also a user - an employee:
  * Employee have custom permission
  * Only employee can view ``` "/api/employee_desk" ```
  * When an employee completed a ticket, an email is sent to the user's email
- Non-authenticated users do not have access to the main endpoints, other than login and register;
- All mailing is done through Celery
- The project is covered with tests

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

## Tests:
In the terminal: <br>
``` sudo docker compose exec web python manage.py test ```

