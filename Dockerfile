#FROM python:3

#WORKDIR /app

#COPY . /app

#RUN pip install --no-cache-dir --upgrade pip &&\
#    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

#EXPOSE 5050

#ENTRYPOINT [ "python", "app.py" ]

FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY . /app