FROM python:3.11-slim

WORKDIR /app

# Оновлюємо тільки pip
RUN pip install --no-cache-dir --upgrade pip

# Копіюємо requirements
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо проект
COPY . .

# Запуск через python -m uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]