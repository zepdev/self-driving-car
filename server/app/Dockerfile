FROM python:3.7-slim-stretch

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]