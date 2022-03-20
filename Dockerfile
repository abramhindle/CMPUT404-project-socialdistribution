FROM python:3.9-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# https://github.com/python-pillow/Pillow/issues/1763
RUN apk add zlib-dev jpeg-dev gcc musl-dev

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

ENTRYPOINT ["./startup.sh"]
