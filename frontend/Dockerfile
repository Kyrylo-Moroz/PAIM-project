# Використовуємо Node.js 20
FROM node:20-alpine

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо весь код
COPY . .

# Копіюємо package.json
COPY package.json ./

# Копіюємо package-lock.json
COPY package-lock.json ./

# Встановлюємо залежності
RUN npm install


# Відкриваємо порт для фронтенду
EXPOSE 3000

# Запускаємо сервер розробки
CMD ["npm", "start"]
