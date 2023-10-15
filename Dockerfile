FROM python:3.8
# TODO (run all this in docker with fastapi webserver)

RUN mkdir /model-server

# Grab our dependencies from the requirements.txt file
COPY requirements.txt /model-server

WORKDIR /model-server

# install of the requirments that we need
RUN pip install -r requirements.txt

# Copy over all of our source files (this includes all the models as well)
COPY ./src/main.py /model-server

CMD ["python3", "main.py"]
