# official python image
from python:3.10-slim

# set work directory
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]