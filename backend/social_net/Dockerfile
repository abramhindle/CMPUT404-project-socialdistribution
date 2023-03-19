FROM python:3.8-slim-buster AS builder
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git procps curl
RUN git clone https://github.com/Sean-Meyers/CMPUT404-project-socialdistribution.git
WORKDIR /CMPUT404-project-socialdistribution/backend/social_net
RUN git pull
RUN pip3 install -r requirements.txt --no-cache-dir
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# FROM --platform=$BUILDPLATFORM python:3.8-slim-buster AS builder
# EXPOSE 8000
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# RUN apt-get update && \
# apt-get upgrade -y && \
# apt-get install -y git procps curl libpq-dev python-dev gcc

# RUN git clone https://github.com/Sean-Meyers/CMPUT404-project-socialdistribution.git
# WORKDIR /CMPUT404-project-socialdistribution/backend/social_net
# RUN git pull

# # COPY . .
# RUN pip3 install pipenv && \
#     pipenv requirements > requirements.txt && \
#     pip3 install -r requirements.txt --no-cache-dir
# COPY ./entrypoint.sh ./
# CMD ["/bin/bash", "./entrypoint.sh"] 