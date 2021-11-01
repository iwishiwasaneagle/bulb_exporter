FROM python:3-slim

WORKDIR /bulb_exporter

COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

ADD src src

ENTRYPOINT ["python3","/bulb_exporter/src/"]