FROM python:3.6
COPY config /unipi_notify/config
COPY unipi_notify.py /unipi_notify
RUN pip install requests
RUN mkdir /unipi_notify/data 
ENTRYPOINT [ "python", "-u", "/unipi_notify/unipi_notify.py"]
