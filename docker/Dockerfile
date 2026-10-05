# syntax=docker/dockerfile:1.4
FROM python:3.8-alpine
WORKDIR /app
COPY proy-requirements.txt proy-requirements.txt
RUN pip3 install -r proy-requirements.txt
COPY . .
CMD ["python3", "proy-app.py"]
