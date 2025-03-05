FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN groupadd -r test_user && useradd -r -g test_user test_user

RUN chown -R test_user:test_user /app

USER test_user

CMD ["python3", "-m", "task_7"]
