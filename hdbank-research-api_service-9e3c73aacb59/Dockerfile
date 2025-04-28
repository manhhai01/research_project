FROM node:20.12.2

WORKDIR /app

COPY package.json .
RUN npm install
RUN npm install -g pm2

COPY . .
EXPOSE 3000
EXPOSE 8000
EXPOSE 5432

#RUN npm run start:dev
RUN npm run prisma:generate
RUN npm run build
# RUN pm2 start dist/main.js --name backend