FROM python:3.11.4

ENV PYTHONBUFFERED=1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/
CMD python manage.py runserver 0.0.0.0:8000
CMD python manage.py tailwind start
