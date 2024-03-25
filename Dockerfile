FROM python:3.9
WORKDIR /app

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir app

COPY app.py app.py
COPY models/ models/
COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 7000

ENTRYPOINT [ "python3", "/app/app.py" ]