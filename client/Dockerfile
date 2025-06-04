FROM node:lts-alpine3.20

ENV COMPOSE_BAKE=true
ENV NODE_ENV=development

WORKDIR /app

COPY package*.json ./

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]