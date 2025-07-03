FROM python:3.11-slim

RUN apt update && apt install -y rclone cron
RUN pip install garminconnect

WORKDIR /app
COPY main.py .

CMD ["python", "main.py"]