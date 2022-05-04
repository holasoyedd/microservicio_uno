FROM python:3.9.6

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "./config/gunicorn/conf.py", "--bind", ":8100", "--chdir", "pruebas", "pruebas.wsgi:application"]