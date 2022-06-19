# Foodgram

## Descpription
The Foodgram service allows everyone to share their recipes with others.
Here you can create/edit/delete your own recipes, add to favorites and shopping list recipes of other authors.
The shopping list can be downloaded as a file and taken with you to the store.
Recipes can be filtered by tags.
It is also possible to subscribe to your favorite author.

### Filling the ENV file
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres (your password)
DB_HOST=db
DB_PORT=5432
```

### Launching a project in containers
- Build and launch containers
    ```
    docker-compose up -d --build
    ```
- Execute the commands one by one:
    ```
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input
    ```

### Link
http://51.250.23.134/recipes

### Authors
Lev Khalyapin
