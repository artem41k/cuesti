FROM python:3.12.1-alpine

WORKDIR /app

STOPSIGNAL SIGKILL

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

RUN chmod +x /app/entrypoint.sh
RUN dos2unix /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]