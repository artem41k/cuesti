FROM node:23-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . ./

RUN npm run build

EXPOSE 8000

CMD ["npx", "serve", "-s", "dist", "-p", "8000"]
# CMD ["npm", "run", "preview"]
