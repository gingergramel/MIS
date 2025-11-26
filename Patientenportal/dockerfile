#basis image
FROM python:3.13

#workdir festlegen
WORKDIR /app

# requirements installation
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN apt-get update -y
RUN apt install unixodbc -y

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:8000/hello || exit 1

CMD ["sh", "docker-entrypoint.sh"]