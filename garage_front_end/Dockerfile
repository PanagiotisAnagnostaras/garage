FROM node:18-alpine

WORKDIR /garage_front_end/

COPY public/ public/
COPY src/ src/
COPY package*.json ./

RUN npm install

CMD ["npm", "start"]