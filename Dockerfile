FROM python:3.10-slim

# Робоча тека всередині контейнера
WORKDIR /app

# Копіюємо тільки requirements і ставимо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо увесь код
COPY . .

# Забезпечуємо, що Python в контейнері не буферить stdout/stderr
ENV PYTHONUNBUFFERED=1

# Запускаємо оркестратор в unbuffered-режимі (-u) однією єдиною CMD
CMD ["python", "-u", "orchestrator.py"]
