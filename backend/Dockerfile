# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо всі файли бекенду
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт для Flask
EXPOSE 5000

# Запускаємо бекенд
CMD ["python", "app.py"]
