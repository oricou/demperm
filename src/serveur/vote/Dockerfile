FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py crontab add

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
