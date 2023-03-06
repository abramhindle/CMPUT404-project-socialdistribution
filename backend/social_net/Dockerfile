
FROM --platform=$BUILDPLATFORM python:3.8-slim-buster AS builder
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git
# WORKDIR /app 
# COPY ./requirements.txt /app
RUN git clone https://github.com/Sean-Meyers/CMPUT404-project-socialdistribution.git
WORKDIR /CMPUT404-project-socialdistribution/backend/social_net
RUN pip3 install -r requirements.txt --no-cache-dir
# COPY . /app
# # USER me
# # WORKDIR /home/me
# WORKDIR /app
# RUN pip3 install pipenv
# # RUN export USERBIN="$(python3 -m site --user-base)"
# # ENV PATH="${USERBIN}:${PATH}"
# RUN apk add git
# RUN git clone https://github.com/Sean-Meyers/CMPUT404-project-socialdistribution.git
# WORKDIR /app/CMPUT404-project-socialdistribution/backend/social_net
# RUN rm Pipfile
# COPY ./Pipfile /app/CMPUT404-project-socialdistribution/backend/social_net/
# # RUN rm Pipfile.lock
# # RUN pipenv lock --verbose
# RUN pipenv install --verbose
# RUN pipenv shell
COPY .env ./
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]