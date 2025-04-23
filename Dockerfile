# Используем официальный образ Python
FROM python:3.12.8-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN python -m venv venv

RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Указываем команду для запуска приложения через Uvicorn
ENTRYPOINT ["./venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

