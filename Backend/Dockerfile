FROM python:3.9

EXPOSE 8080

WORKDIR /app

COPY app.py .

RUN chmod +x /app/app.py

CMD ["pip", "install", "-r", "/app/requirements.txt"]

CMD ["apt", "install", "python3-all"]

CMD ["python3", "/app/app.py", "8080"]

