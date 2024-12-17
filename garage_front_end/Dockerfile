FROM node:18-alpine

WORKDIR /garage_front_end/

COPY package*.json ./

RUN npm install

COPY public/ public/
COPY src/ src/

CMD ["npm", "start"]