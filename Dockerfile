FROM ubuntu:latest

EXPOSE 3332

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN export PYTHONPATH=$PYTHONPATH:$(pwd)

CMD ["python3", "-m", "uvicorn", "health_journal.main:app", "--reload", "--host", "0.0.0.0", "--port", "3332"]