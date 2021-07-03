# syntax=docker/dockerfile:1
FROM python:3.9.5
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip 
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin
COPY . /code/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

