FROM python:3.8-slim
RUN mkdir /usr/src/unipi-notify
WORKDIR /usr/src/unipi-notify
RUN mkdir data 
COPY unipi-notify.py .
COPY requirements.txt .
COPY config ./config
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "-u", "unipi-notify.py"]
