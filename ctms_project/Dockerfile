FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 manage.py migrate --noinput && \
    python3 manage.py seed_users && \
    python3 manage.py seed_data && \
    python3 manage.py collectstatic --noinput
CMD ["gunicorn", "ctms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
