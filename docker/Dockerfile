# syntax=docker/dockerfile:1.4
FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY api/app.py .

CMD ["python3", "app.py"]
