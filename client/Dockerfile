FROM node:lts-alpine3.20

ENV COMPOSE_BAKE=true

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]