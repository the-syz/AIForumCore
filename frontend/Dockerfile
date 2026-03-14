FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* .
# 配置阿里云npm镜像源
RUN npm config set registry https://registry.npmmirror.com && \
    npm install

COPY . .

CMD ["npm", "run", "dev"]