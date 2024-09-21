FROM ubuntu:22.04

EXPOSE 8080

WORKDIR $HOME

COPY app.py .

RUN chmod +x $HOME/app.py

RUN ["python3 app.py 8080"]

