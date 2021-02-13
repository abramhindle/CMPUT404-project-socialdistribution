FROM node:alpine
WORKDIR /app/frontend
ENV PATH /app/frontend/node_modules/.bin:$PATH
COPY package.json /app/frontend
RUN npm install

COPY . ./
expose 3000
CMD ["npm", "start"]


