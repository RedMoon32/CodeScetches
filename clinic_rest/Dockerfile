FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gettext && apt-get clean


COPY ./requirements.txt .
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#--no-cache-dir
WORKDIR /app

COPY ./ ./

ARG backend_databese_host=10.91.45.222
ENV DATA_BASE=$backend_databese_host

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

