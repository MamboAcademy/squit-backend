#base image will be a python image
FROM python:3.8

#Create a folder called "app" in the container to put all the folders from the repository to the container
RUN mkdir /app
#"app" will be the working directory. Any RUN, CMD, ADD, COPY or ENTRYPOINT will be executed there
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "./app.py" ]