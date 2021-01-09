FROM python:3.9.0

WORKDIR /home/

RUN echo "testing1234"

RUN git clone https://www.github.com/svstar94/study_django.git

WORKDIR /home/study_django/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient



EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --settings=pragmatic.settings.deploy --noinput && python manage.py migrate --settings=pragmatic.settings.deploy && gunicorn pragmatic.wsgi --env DJANGO_SETTINGS_MODULE=pragmatic.settings.deploy --bind 0.0.0.0:8000"]
