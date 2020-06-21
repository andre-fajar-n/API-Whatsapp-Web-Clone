FROM python:3
MAINTAINER AndreFN "andrenugroho395@gmail.com"
RUN mkdir -p /demo
RUN mkdir -p /demo/storage/log
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]