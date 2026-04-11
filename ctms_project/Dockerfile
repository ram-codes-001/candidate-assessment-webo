FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py migrate --noinput && \
    python manage.py seed_users && \
    python manage.py seed_data && \
    python manage.py collectstatic --noinput
CMD ["gunicorn", "ctms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
