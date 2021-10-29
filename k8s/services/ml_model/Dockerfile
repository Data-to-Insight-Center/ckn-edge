FROM python:3.7

WORKDIR src
COPY . /src

RUN pip install -r requirements.txt

EXPOSE 11000

CMD ["python", "server.py"]