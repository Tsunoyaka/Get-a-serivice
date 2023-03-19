FROM python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings



COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN make migrate

EXPOSE 8000

COPY ./entrypoint.sh .

CMD [ "python3","manage.py","runserver","0.0.0.0:8000" ]
