FROM python:3.6.3

# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /usr/src/app
# ENTRYPOINT [ "flask" ]
# CMD ["run", "--host=localhost"]
CMD ["python", "manage.py", "runserver"]