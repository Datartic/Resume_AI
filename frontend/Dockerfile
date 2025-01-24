FROM node:16

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . ./

# Use the development server with hot reloading
CMD ["npm", "start"]
