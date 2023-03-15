python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable

python manage.py createsuperuser \
        --noinput \
        --email admin@example.com\
        --username admin\
        --last_name admin\
        --surname admin\


$@