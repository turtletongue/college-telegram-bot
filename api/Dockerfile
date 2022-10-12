FROM python:3.7.13-alpine3.16

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 3030

CMD ["python3", "app.py"]