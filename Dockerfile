# Базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .
#RUN sleep 5 && alembic upgrade head

# Открываем порт (если FastAPI, по умолчанию 8000)
EXPOSE 9000

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]

# CMD ["uvicorn", "app:fast_api_app", "--host", "0.0.0.0", "--port", "9000"]
#CMD ["python3", "app.py"]
