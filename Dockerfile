FROM node:17-alpine3.14

RUN if [ -z "$IS_DEV_CONTAINER" ]; then \
  apk update && apk add curl git bash && \
  curl https://cli-assets.heroku.com/install.sh | sh; \
  fi

WORKDIR /data/src/app

COPY src/app/package*.json ./

RUN npm ci

COPY src/app/ ./

RUN npm run build

WORKDIR /data/src/server/

COPY src/server/package*.json ./

RUN npm install

WORKDIR /data/

COPY ./ ./

WORKDIR /data/src/server/

EXPOSE 3000 3001

CMD ["ln", "-s", "../app/build", "build", "&&", "npm", "start"]