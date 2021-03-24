FROM python:3

ENV PYTHONUNBUFFERED=1
WORKDIR /Import_Export
COPY    requirements.txt /Import_Export/
RUN pip install -r requirements.txt
COPY . /Import_Export/