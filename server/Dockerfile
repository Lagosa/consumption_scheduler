FROM python:3.11.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./server/requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./server/ /code/

EXPOSE 8000

ENTRYPOINT ["sh", "-c","python /code/manage.py makemigrations && python /code/manage.py migrate && python /code/manage.py runserver 0.0.0.0:8000"]
