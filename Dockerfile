FROM python:3.11-slim

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём директорию для данных
RUN mkdir -p /app/data && chmod 777 /app/data

# Переменные окружения
ENV DATA_DIR=/app/data
ENV PYTHONUNBUFFERED=1

# Запускаем Python бота
CMD ["python", "bot.py"]
