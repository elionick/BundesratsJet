FROM python:3
RUN apt update && apt install -y firefox-esr
WORKDIR /main
COPY requirements.txt /main/
RUN pip install -r requirements.txt
COPY . /main
ENTRYPOINT python /main/main.py