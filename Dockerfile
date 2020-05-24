FROM python:3.6
RUN pip install requests
COPY config /unipi_notify/config
RUN mkdir /unipi_notify/data 
COPY unipi_notify.py /unipi_notify
ENTRYPOINT [ "python", "-u", "/unipi_notify/unipi_notify.py"]
