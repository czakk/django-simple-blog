FROM python:3.11.4

ENV PYTHONBUFFERED=1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
CMD ["python", "manage.py", "tailwind", "start"]
