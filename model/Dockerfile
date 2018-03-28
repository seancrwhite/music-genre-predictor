# Format: FROM    repository[:version]
FROM       ubuntu:latest

COPY . /model
WORKDIR /model

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["model.py"]