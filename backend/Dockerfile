FROM python:3.10-alpine
WORKDIR /app
COPY ../requirements/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
CMD ["gunicorn","backend.wsgi:application","--bind","0:8000"]
