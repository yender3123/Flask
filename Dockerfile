FROM python:3.9-slim

# Установим рабочую директорию
WORKDIR /app

# Скопируем файлы приложения в контейнер
COPY . /app

# Установим зависимости
RUN pip install --no-cache-dir Flask

# Укажем порт, который будет слушать приложение
EXPOSE 8080

# Команда для запуска приложения
CMD ["python", "main.py"]