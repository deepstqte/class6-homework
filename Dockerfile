FROM ubuntu:latest

COPY requirements.txt ./

RUN apt update && \
    apt install -y python3 \
                   python3-pip && \
    pip3 install -r requirements.txt

COPY housing.data ./
COPY app.py ./

EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:server",  "--workers", "4"]
